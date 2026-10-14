#!/usr/bin/env python3
"""Configure Android launcher and visible TTS engines without background media services."""
import sys,shutil,xml.etree.ElementTree as ET
from pathlib import Path
project=Path(sys.argv[1]);repo=Path(__file__).resolve().parents[1]
ns='http://schemas.android.com/apk/res/android';ET.register_namespace('android',ns)
manifest=project/'android/app/src/main/AndroidManifest.xml';tree=ET.parse(manifest);root=tree.getroot()
root.find('application').set(f'{{{ns}}}label','Emisyon Saha Talimatları')
queries=root.find('queries')
if queries is None:queries=ET.SubElement(root,'queries')
intent=ET.SubElement(queries,'intent');ET.SubElement(intent,'action',{f'{{{ns}}}name':'android.intent.action.TTS_SERVICE'})
ET.indent(tree);tree.write(manifest,encoding='utf-8',xml_declaration=True)
res=project/'android/app/src/main/res'
for folder in (repo/'assets/branding').glob('mipmap-*'):shutil.copytree(folder,res/folder.name,dirs_exist_ok=True)
for directory in res.glob('mipmap-anydpi*'):
 for f in directory.glob('ic_launcher*.xml'):f.unlink()
(res/'drawable-nodpi').mkdir(exist_ok=True);shutil.copyfile(repo/'assets/branding/launcher.png',res/'drawable-nodpi/emission_mark.png')
(res/'mipmap-anydpi-v26').mkdir(exist_ok=True)
(res/'mipmap-anydpi-v26/ic_launcher.xml').write_text('<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android"><background android:drawable="@color/launcher_background"/><foreground android:drawable="@drawable/emission_mark"/></adaptive-icon>')
(res/'values/launcher_colors.xml').write_text('<resources><color name="launcher_background">#123349</color></resources>')
print('Android title, chimney icon and TTS queries configured')
