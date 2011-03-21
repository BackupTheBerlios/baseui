#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

#===============================================================================
# BuildHelpers 
# by Mark Muzenhardt, published under LGPL license.
#===============================================================================

import sys, os, imp, shutil

from pprint import pprint


def get_winGTKdir():
    # Fetches gtk2 path from registry.
	
    import _winreg
    import msvcrt

    try:
        k = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, "Software\\GTK\\2.0")
    except EnvironmentError, inst:
        print "You must install the GTK+ 2.0 Runtime Environment to run this programm,", inst
        while not msvcrt.kbhit():
            pass
        return None
    else:
        gtkdir = _winreg.QueryValueEx(k, "Path")
        gtkversion = _winreg.QueryValueEx(k, "Version")
        import os
        os.environ['PATH'] += ";%s/lib;%s/bin" % (gtkdir[0], gtkdir[0])
        return gtkdir[0] + '\\'
        

def get_rpm(**kwargs):
	# This stuff is simply a try to capture rpm-support, but not ready yet!
	
	rpm_text = """\
# This is a sample spec file for wget

%define _topdir	 	/home/strike/mywget
%define name			wget 
%define release		1
%define version 	1.12
%define buildroot %{_topdir}/%{name}-%{version}-root

BuildRoot:	%{buildroot}
Summary: 		GNU wget
License: 		GPL
Name: 			%{name}
Version: 		%{version}
Release: 		%{release}
Source: 		%{name}-%{version}.tar.gz
Prefix: 		/usr
Group: 			Development/Tools

%description
The GNU wget program downloads files from the Internet using the command-line.

%prep
%setup -q

%build
./configure
make

%install
make install prefix=$RPM_BUILD_ROOT/usr

%files
%defattr(-,root,root)
/usr/local/bin/wget

%doc %attr(0444,root,root) /usr/local/share/man/man1/wget.1"""
	return rpm_text
	
	
def get_deb(**kwargs):
	# This stuff is simply a try to capture deb-support, but not yet ready!
	
	deb_text = """\
Package: acme
Version: 1.0
Section: web 
Priority: optional
Architecture: all
Essential: no
Depends: libwww-perl, acme-base (>= 1.2)
Pre-Depends: perl 
Recommends: mozilla | netscape  
Suggests: docbook 
Installed-Size: 1024
Maintainer: Joe Brockmeier [jzb@dissociatedpress.net]
Conflicts: wile-e-coyote
Replaces: sam-sheepdog
Provides: acme
Description: The description can contain free-form text
             describing the function of the program, what
             kind of features it has, and so on..."""
	return deb_text
	
	
def get_nsi(**kwargs):
	# This works fine to make an installer for windows with NSIS.
	
    python_version = sys.version[:3]
    
    nsi_text = """\
;------------------------------------------------------------------------------

  !include "MUI2.nsh"

;------------------------------------------------------------------------------
Name "%(APP_NAME)s"
; Icon "../res/%(APP_ICON)s"

; The file to write
OutFile "../dist/%(APP_NAME)s v%(APP_VERSION)s.exe"

; The default installation directory
InstallDir "$PROGRAMFILES\%(APP_NAME)s"

; Request application privileges for Windows Vista
RequestExecutionLevel highest

; This makes the Installer-Icon.
!define MUI_ICON "../res/%(APP_ICON)s"

; Pages -----------------------------------------------------------------------
  !insertmacro MUI_PAGE_LICENSE "..\doc\source\license.rst"
  !insertmacro MUI_PAGE_DIRECTORY
  !insertmacro MUI_PAGE_INSTFILES

  !insertmacro MUI_UNPAGE_CONFIRM
  !insertmacro MUI_UNPAGE_INSTFILES


; Languages -------------------------------------------------------------------
  !insertmacro MUI_LANGUAGE "German"


; The stuff to install --------------------------------------------------------
Section "Installer Section" ;No components page, name is not important

  ; Set output path to the installation directory.
  SetOutPath $INSTDIR

  ; Put file there
  File /r "../build/exe.""" + "%s-%s" % (sys.platform, python_version) + """\*"

  ; Make uninstaller
  WriteUninstaller $INSTDIR\uninstaller.exe

  CreateDirectory "$SMPROGRAMS\%(APP_NAME)s"
  CreateShortCut "$SMPROGRAMS\%(APP_NAME)s\%(APP_NAME)s.lnk" "$INSTDIR\%(APP_NAME)s.exe"
  CreateShortCut "$SMPROGRAMS\%(APP_NAME)s\Uninstall.lnk" "$INSTDIR\uninstaller.exe"
  CreateShortCut "$DESKTOP\%(APP_NAME)s.lnk" "$INSTDIR\%(APP_NAME)s.exe"

  ; Add to the software dialog of windows
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\%(APP_NAME)s" \\
                   "DisplayName" "%(APP_NAME)s %(APP_VERSION)s" 
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\%(APP_NAME)s" \\
                   "DisplayIcon" "$INSTDIR\\res\\%(APP_ICON)s"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\%(APP_NAME)s" \\
                   "UninstallString" "$INSTDIR\uninstaller.exe"
SectionEnd ; end the section


; The stuff to uninstall ------------------------------------------------------
Section "un.Uninstaller Section"
  Delete $INSTDIR\uninstaller.exe
  RMDir /r "$SMPROGRAMS\%(APP_NAME)s"
  Delete "$DESKTOP\%(APP_NAME)s.lnk"

  !include "%(APP_NAME)s.log"
  
  ; Remove from the software dialog of windows
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\%(APP_NAME)s"
SectionEnd
;------------------------------------------------------------------------------"""
    return nsi_text % kwargs
      
        
def get_revision():
    # The easiest way to get the revision control system is to look up the directorys!
    # os.getcwd()
    dir_list = os.listdir('.')
    try:
        if '.hg' in dir_list:
            out = os.popen('hg log')
            log = out.read()
            log_list = (log.split('\n'))
            change_list = []
            for line in log_list:
                if line.startswith('changeset'):
                    changeset = line.split(':')
                    change_list.append(int(changeset[1]))
            app_revision = str(max(change_list))
        elif '.svn' in dir_list:
        
            import pysvn

            client = pysvn.Client()
            entry = client.info('.')
            app_revision = str(entry.revision.number)
    except Exception, inst:
        print str(inst)
        raw_input('>')
        app_revision = ''
    return app_revision
    
    
def makeGTK(gtk_dir, pathname, build_dir, localized=False):
    if sys.platform.startswith('win'):
        os.system('xcopy ' + gtk_dir + 'bin\\*.dll "' + pathname + build_dir + '" /E /Y')
        os.system('xcopy ' + gtk_dir + 'lib\\* "' + pathname + build_dir + 'lib\\" /E /Y')
        os.system('xcopy ' + gtk_dir + 'etc\\* "' + pathname + build_dir + 'etc\\" /E /Y')
        os.system('xcopy ' + gtk_dir + 'share\\themes\\* "' + pathname + build_dir + 'share\\themes\\" /E /Y')
        
        if localized == True:
            os.system('xcopy ' + gtk_dir + 'share\\locale\\* "' + pathname + build_dir + 'share\\locale\\" /E /Y')
        

def makeResources(pathname, build_dir):
    if sys.platform.startswith('win'):
        os.system('xcopy "' + pathname + '\\res\\*" "' + pathname + build_dir + 'res\\" /E /Y')
        #usr is no ressource any longer, because database-config should not be uninstalled!
        #os.system('xcopy "' + pathname + '\\usr\\*" "' + pathname + build_dir + 'usr\\" /E /Y')
        os.system('xcopy "' + pathname + '\\bin\\*" "' + pathname + build_dir + 'bin\\" /E /Y')
    if sys.platform.startswith('linux'):
        os.system('cp -R ' + pathname + '/res/*' + pathname + build_dir + 'res/')
        #same as above (under windows).
        #os.system('cp -R ' + pathname + '/usr/*' + pathname + build_dir + 'usr/')
        os.system('cp -R ' + pathname + '/bin/*' + pathname + build_dir + 'bin/')
        
        
def makeAbout(tpl_path, svg_path, author, version, revision, license, make_png=False):
    # Build about.svg -------------------------------------------------------------
    try:
        image_file = open(tpl_path, 'r')
    except Exception, inst:
        print inst
        return
        
    file_content = image_file.read()
    image_file.close()

    replacement_dict = {'%APP_AUTHOR%': author,
                        '%APP_VERSION%': version,
                        '%APP_REVISION%': revision,
                        '%APP_LICENSE%': license}
                        
    for key in replacement_dict:
        file_content = file_content.replace(key, replacement_dict[key])
    
    output_file = open(svg_path, 'w')
    output_file.write(file_content)
    output_file.close()
    
    if make_png == True:
        opts_dict = {'programfiles': os.environ['PROGRAMFILES'],
                     'thisdir': os.getcwd(),
                     'svgpath': svg_path,
                     'pngpath': 'res\\about.png'}
        
        os.chdir("%(programfiles)s\\Inkscape\\" % opts_dict)
        command = 'inkscape.exe -f "%(thisdir)s\\%(svgpath)s" -e "%(thisdir)s\\%(pngpath)s"' % opts_dict
        os.popen(command)
        
    
def makeSphinx(pathname, build_dir):
    # Make and copy documentation ---------------------------------------------
    os.chdir(pathname + '\\doc\\')
    doc_config = imp.load_source('make', 'make.py')
    os.chdir(pathname)

    os.system('xcopy "' + pathname + '\\doc\\build\\html" "' + pathname + build_dir + 'doc\\html\\" /E /Y')
    os.system('xcopy "' + pathname + '\\doc\\build\\htmlhelp" "' + pathname + build_dir + 'doc\\htmlhelp\\" /E /Y')
    os.system('xcopy "' + pathname + '\\doc\\build\\latex\*.pdf" "' + pathname + build_dir + 'doc\\" /E /Y')


def makeAutorun():
    text = """\
[Autorun]
ShellExecute=startup\start.exe
UseAutoplay=1"""
    
    
def makeNSI(pathname, build_dir, app_name, app_version, app_icon=''):
    # Make installer with NSIS ------------------------------------------------
    nsi_file = open("%s\\build\\%s.nsi" % (pathname, app_name), 'w')
    nsi_file.write(get_nsi(APP_NAME=app_name, APP_VERSION=app_version, APP_ICON=app_icon))
    nsi_file.close()

    # Make uninstaller first --------------------------------------------------   
    os.chdir(pathname + '\\build\\')
    output_file = open('%s.log' % app_name, 'w')
    upper_text = ''
    lower_text = ''
    os.chdir(pathname + build_dir)
    
    iter = os.walk('.', topdown=False)
    for tuple in iter:
        dirpath   = tuple[0]
        dirnames  = tuple[1]
        filenames = tuple[2]

        if filenames <> []:
            for filename in filenames:
                if dirpath <> '.':
                    filename = "\%s" % filename
                log_line = 'Delete "$INSTDIR\%s%s"\n' % (dirpath[2:], filename)
                upper_text += log_line
        
        if dirnames <> []:
            for dirname in dirnames:
                if dirpath <> '.':
                    dirname = "\%s" % dirname

                log_line = 'RMDir "$INSTDIR\%s%s"\n' % (dirpath[2:], dirname)
                lower_text += log_line
    lower_text += 'RMDir "$INSTDIR"'
        
    output_file.write(upper_text + lower_text)
    output_file.close()
    os.chdir(pathname)
    
    # Now, build the whole installer ------------------------------------------
    try:
        os.mkdir('dist')
    except Exception, inst:
        print str(inst)
        
    ProgramFiles = os.getenv("ProgramFiles")
    makeNSISw = '"' + ProgramFiles + '\\NSIS\\makensisw.exe" "build\\%s.nsi"' % app_name
    os.popen('"%s"' % makeNSISw)
    
    
    
    