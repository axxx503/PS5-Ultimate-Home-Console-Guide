#!/usr/bin/env python3
"""PS5 Release Tracker: inspect and stage upstream releases on a PC. No PS5 writes."""
from __future__ import annotations
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import queue
import re
import threading
import urllib.error
import urllib.request
from urllib.parse import urlparse
import tkinter as tk
from tkinter import ttk, messagebox

PROJECTS = {
    "ps5sx2": ("PS5SX2", "Swordpdf", "PS5SX2"),
    "porpoise": ("Porpoise / Dolphin", "elripalda", "Porpoise-Dolphin-Emulator-for-PS5"),
    "cemu": ("PS5CEMU-HAR", "premohq", "PS5CEMU-HAR"),
    "x360": ("PS5X360", "BrinooTk", "PS5X360"),
    "xpsemu": ("XPSemu", "ZiZc3", "XPSemu"),
}
STAGING = Path(__file__).resolve().parent / "staging"
HEADERS = {"User-Agent": "PS5-Release-Tracker/1.2 (manual staging)", "Accept": "application/vnd.github+json"}

def safe_name(value: str) -> str:
    name=Path(value).name
    if name != value or not re.fullmatch(r"[A-Za-z0-9._+() -]{1,180}", name) or name.startswith("."):
        raise ValueError("Unsafe release asset name")
    return name

def api_json(owner: str, repo: str) -> dict:
    if (owner, repo) not in {(x[1], x[2]) for x in PROJECTS.values()}:
        raise ValueError("Project not on allowlist")
    req=urllib.request.Request(f"https://api.github.com/repos/{owner}/{repo}/releases/latest",headers=HEADERS)
    with urllib.request.urlopen(req,timeout=15) as response:
        if response.status!=200: raise RuntimeError(f"GitHub HTTP {response.status}")
        return json.loads(response.read(3_000_000))

def choose_asset(release: dict) -> dict | None:
    """Choose an upstream installable binary, never GitHub-generated source archives."""
    assets=[]
    for a in release.get('assets',[]):
        name=a.get('name','');url=a.get('browser_download_url','')
        if not (name.lower().endswith(('.zip','.elf')) and (urlparse(url).scheme=='https' and urlparse(url).hostname=='github.com')):continue
        try:safe_name(name)
        except ValueError:continue
        n=name.lower()
        if any(term in n for term in ('source-code','source_code','symbols','debug-symbols','source.zip','sources.zip','-src.zip')):continue
        score= (10 if 'ppsa' in n else 0)+(4 if n.endswith('.zip') else 0)+(2 if ('release' in n or 'ps5' in n) else 0)
        assets.append((score,name,a))
    return sorted(assets,key=lambda x:(-x[0],x[1]))[0][2] if assets else None

def snapshot(key: str) -> dict:
    label,owner,repo=PROJECTS[key]
    r=api_json(owner,repo)
    a=choose_asset(r)
    return {'key':key,'label':label,'tag':r.get('tag_name','unknown'),'published_at':r.get('published_at',''),
            'release_url':r.get('html_url',f'https://github.com/{owner}/{repo}/releases'),
            'asset':None if a is None else {'name':a['name'],'url':a['browser_download_url'],'size':a.get('size',0)}}

def stage(item: dict,folder:Path=STAGING) -> tuple[Path, str]:
    asset=item.get('asset')
    if asset is None: raise ValueError('No suitable installable asset. Open upstream release page and review manually.')
    name=safe_name(asset['name'])
    url=asset['url']
    if not (urlparse(url).scheme=='https' and urlparse(url).hostname=='github.com'):raise ValueError('Release asset URL is not the expected GitHub URL')
    out_dir=folder/item['key']/safe_name(item['tag'].replace('/','_'))
    out_dir.mkdir(parents=True,exist_ok=True)
    target=out_dir/name;temp=out_dir/(name+'.part')
    if target.exists() or temp.exists():raise FileExistsError(f'Output already exists: {target} (refusing overwrite)')
    h=hashlib.sha256();count=0
    req=urllib.request.Request(url,headers={'User-Agent':HEADERS['User-Agent']})
    try:
        with urllib.request.urlopen(req,timeout=45) as response,open(temp,'xb') as f:
            # urllib follows GitHub signed HTTPS release-asset redirect, but rejects non-HTTPS.
            if not response.geturl().startswith('https://'):raise ValueError('Refusing unencrypted redirect')
            while True:
                buf=response.read(1024*1024)
                if not buf:break
                count+=len(buf)
                if count>2*1024**3:raise ValueError('File exceeds 2 GiB staging limit')
                f.write(buf);h.update(buf)
        if asset.get('size') and count!=asset['size']:raise IOError(f'Unexpected size: expected {asset["size"]}, got {count}')
        temp.rename(target)
        metadata={'project':item['label'],'tag':item['tag'],'asset':name,'source_url':url,'source_release':item['release_url'],
          'sha256_calculated_locally':h.hexdigest(),'size_bytes':count,'downloaded_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
          'verification_warning':'SHA-256 is local integrity record only; this is NOT verified against a publisher signature.'}
        (out_dir/'STAGING-MANIFEST.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        return target,h.hexdigest()
    finally:
        if temp.exists():temp.unlink()

class App:
    def __init__(self,root,lang='en'):
        self.root=root;self.lang=lang;self.results={};self.q=queue.Queue()
        ar=lang=='ar';root.title('PS5 Release Tracker 1.2 - '+('مراجعة التحديثات' if ar else 'Safe update staging'))
        root.geometry('880x560');root.minsize(690,460)
        style=ttk.Style(root)
        if 'clam' in style.theme_names():style.theme_use('clam')
        header=ttk.Frame(root,padding=18);header.pack(fill='x')
        ttk.Label(header,text='PS5 RELEASE TRACKER',font=('Segoe UI',19,'bold')).pack(anchor='w')
        ttk.Label(header,text=('يفحص الإصدارات وينزل ملفاً واحداً بعد موافقتك. لا يحدث PS5 تلقائيًا.' if ar else
           'Check release versions and stage files on this PC. Never modifies your PS5.'),font=('Segoe UI',10)).pack(anchor='w',pady=4)
        cols=('project','version','asset','status')
        self.table=ttk.Treeview(root,columns=cols,show='headings',height=11,selectmode='browse')
        titles=['Project','Latest tag','Installable asset','Status']
        for col,title,w in zip(cols,titles,[190,150,360,160]):self.table.heading(col,text=title);self.table.column(col,width=w,anchor='w')
        for key,(label,_,_) in PROJECTS.items():self.table.insert('', 'end',iid=key,values=(label,'—','—','Not checked'))
        self.table.pack(fill='both',expand=True,padx=18,pady=7)
        foot=ttk.Frame(root,padding=16);foot.pack(fill='x')
        self.b_check=ttk.Button(foot,text=('فحص الإصدارات' if ar else 'Check Releases'),command=self.check);self.b_check.pack(side='left',padx=5)
        self.b_stage=ttk.Button(foot,text=('تنزيل الاختيار إلى الكمبيوتر' if ar else 'Stage Selected'),command=self.download);self.b_stage.pack(side='left',padx=5)
        ttk.Button(foot,text=('فتح مجلد التحميل' if ar else 'Open Staging Folder'),command=self.show_folder).pack(side='left',padx=5)
        ttk.Button(foot,text=('صفحة إصدار المشروع' if ar else 'Open Release Page'),command=self.open_page).pack(side='left',padx=5)
        self.status=tk.StringVar(value=('اختر فحص الإصدارات أولاً.' if ar else 'Start by checking releases.'))
        ttk.Label(root,textvariable=self.status,wraplength=830,padding=10).pack(fill='x')
        ttk.Label(root,text=('تنبيه: البناء المعدل على USB قد يتعطل إذا ثبتت فوقه نسخة رسمية.' if ar else
            'Warning: stock updates may revert custom USB path patches. Back up first.'),foreground='#af501a',padding=(18,0,18,12)).pack(anchor='w')
        self.root.after(150,self.poll)
    def task(self,action,worker):
        self.b_check['state']='disabled';self.b_stage['state']='disabled';self.status.set(action)
        def run():
            try:self.q.put(('ok',worker()))
            except Exception as e:self.q.put(('error',str(e)))
        threading.Thread(target=run,daemon=True).start()
    def check(self):
        def worker():
            rows={}
            for key in PROJECTS:
                try:rows[key]=snapshot(key)
                except Exception as e:rows[key]=str(e)
            return ('check',rows)
        self.task('Checking GitHub Releases...',worker)
    def download(self):
        sel=self.table.selection()
        if not sel:return messagebox.showinfo('Select', 'Choose a project row first.')
        obj=self.results.get(sel[0]);
        if not obj or not obj.get('asset'):return messagebox.showwarning('No asset','Check releases or open upstream release page for manual review.')
        if not messagebox.askyesno('Stage on PC only',f"Download {obj['asset']['name']} to this PC?\n\nThis will NOT install anything on the PS5."):return
        self.task('Downloading release asset...',lambda:('stage',stage(obj)))
    def open_page(self):
        import webbrowser
        sel=self.table.selection()
        if not sel:return
        key=sel[0];url=self.results.get(key,{}).get('release_url') or f'https://github.com/{PROJECTS[key][1]}/{PROJECTS[key][2]}/releases'
        webbrowser.open(url)
    def show_folder(self):
        STAGING.mkdir(exist_ok=True)
        if os.name=='nt':os.startfile(STAGING)
        else:self.status.set('Staging: '+str(STAGING))
    def poll(self):
        try:
            while True:
                status,payload=self.q.get_nowait()
                self.b_check['state']='normal';self.b_stage['state']='normal'
                if status=='error':self.status.set('Error: '+payload);messagebox.showerror('Error',payload)
                elif payload[0]=='check':
                    for key,item in payload[1].items():
                        if isinstance(item,str): self.table.item(key,values=(PROJECTS[key][0],'—','—','Error: '+item[:45]));continue
                        self.results[key]=item
                        a=item['asset'];self.table.item(key,values=(item['label'],item['tag'],a['name'] if a else 'No safe binary asset','Ready' if a else 'Review manually'))
                    self.status.set('Release check complete. Review upstream notes before staging.')
                elif payload[0]=='stage':
                    path,sha=payload[1];self.status.set('Staged on this PC: '+str(path)+' | SHA-256: '+sha)
                    messagebox.showinfo('Staging complete','Saved to: '+str(path)+'\n\nNO files changed on PS5.\nLocal SHA-256: '+sha)
        except queue.Empty:pass
        self.root.after(150,self.poll)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--lang',choices=['en','ar'],default='en');ap.add_argument('--check',action='store_true');ap.add_argument('--stage',choices=list(PROJECTS))
    args=ap.parse_args()
    if args.check:
        for key in PROJECTS:
            try: print(json.dumps(snapshot(key),indent=2))
            except Exception as e:print(f'{key}: {e}')
    elif args.stage:
        v=snapshot(args.stage)
        if not v['asset']:raise SystemExit('No installable asset: '+v['release_url'])
        print('Staged:',stage(v))
    else:
        root=tk.Tk();App(root,args.lang);root.mainloop()
if __name__=='__main__':main()
