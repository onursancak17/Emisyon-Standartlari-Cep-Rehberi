#!/usr/bin/env python3
"""Apply display name, launcher artwork and background media configuration."""
import shutil
import sys
from pathlib import Path
import xml.etree.ElementTree as ET

project = Path(sys.argv[1])
repo = Path(__file__).resolve().parents[1]
android = 'http://schemas.android.com/apk/res/android'
ET.register_namespace('android', android)
manifest = project / 'android/app/src/main/AndroidManifest.xml'
tree = ET.parse(manifest)
root = tree.getroot()
for permission in ['WAKE_LOCK', 'FOREGROUND_SERVICE', 'FOREGROUND_SERVICE_MEDIA_PLAYBACK']:
    ET.SubElement(root, 'uses-permission', {f'{{{android}}}name':f'android.permission.{permission}'})
app=root.find('application')
app.set(f'{{{android}}}label','@string/app_name')
activity=app.find('activity')
activity.set(f'{{{android}}}name','com.ryanheise.audioservice.AudioServiceActivity')
service=ET.SubElement(app,'service',{f'{{{android}}}name':'com.ryanheise.audioservice.AudioService',f'{{{android}}}foregroundServiceType':'mediaPlayback',f'{{{android}}}exported':'true'})
intent=ET.SubElement(service,'intent-filter')
ET.SubElement(intent,'action',{f'{{{android}}}name':'android.media.browse.MediaBrowserService'})
receiver=ET.SubElement(app,'receiver',{f'{{{android}}}name':'com.ryanheise.audioservice.MediaButtonReceiver',f'{{{android}}}exported':'true'})
intent=ET.SubElement(receiver,'intent-filter')
ET.SubElement(intent,'action',{f'{{{android}}}name':'android.intent.action.MEDIA_BUTTON'})
ET.indent(tree)
tree.write(manifest,encoding='utf-8',xml_declaration=True)
res=project/'android/app/src/main/res'
(res/'values').mkdir(parents=True,exist_ok=True)
(res/'values/strings.xml').write_text('<?xml version="1.0" encoding="utf-8"?><resources><string name="app_name">Emisyon İmisyon Ölçüm Standartları</string></resources>')
for folder in (repo/'assets/branding').glob('mipmap-*'):
    shutil.copytree(folder,res/folder.name,dirs_exist_ok=True)
# Remove template adaptive icon definitions so Android uses the new artwork at every density.
for directory in res.glob('mipmap-anydpi*'):
    for f in directory.glob('ic_launcher*.xml'):f.unlink()
(res/'drawable-nodpi').mkdir(exist_ok=True)
shutil.copyfile(repo/'assets/branding/launcher.png',res/'drawable-nodpi/emission_mark.png')
(res/'mipmap-anydpi-v26').mkdir(exist_ok=True)
(res/'mipmap-anydpi-v26/ic_launcher.xml').write_text('<?xml version="1.0" encoding="utf-8"?><adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android"><background android:drawable="@color/launcher_background"/><foreground android:drawable="@drawable/emission_mark"/></adaptive-icon>')
(res/'values/launcher_colors.xml').write_text('<resources><color name="launcher_background">#102A43</color></resources>')
print('Android label, industrial launcher and media service configured')
