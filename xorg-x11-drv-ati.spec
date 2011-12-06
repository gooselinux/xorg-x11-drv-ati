%define tarball xf86-video-ati
%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir	%{moduledir}/drivers
#%define gitdate 20100219
#%define gitversion 1b7e9a2e5

Summary:   Xorg X11 ati video driver
Name:      xorg-x11-drv-ati
Version:   6.13.0
Release:   6%{?dist}
URL:       http://www.x.org
License:   MIT
Group:     User Interface/X Hardware Support
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:    http://www.x.org/pub/individual/driver/%{tarball}-%{version}.tar.bz2
#Source0: %{tarball}-%{gitdate}.tar.xz
# unlike the other drivers, radeon.xinf is generated
Source1:    mkxinf
Source2:    radeon-firmware-2.tar.bz2

Patch2:     radeon-server-clone.patch
Patch3:     radeon-kms-add-uevent.patch
Patch6:     radeon-6.9.0-bgnr-enable.patch
Patch10:    radeon-6.12.2-lvds-default-modes.patch
Patch13:    fix-default-modes.patch
Patch14:    radeon-rn50-no-xv.patch
Patch15:    radeon-rn50-fix-cloning.patch
Patch16:    radeon-rn50-powerpc-fixes.patch

ExcludeArch: s390 s390x

BuildRequires: python
BuildRequires: xorg-x11-server-devel >= 1.7.5-5
BuildRequires: mesa-libGL-devel >= 6.4-4
BuildRequires: libdrm-devel >= 2.4.17-1
BuildRequires: kernel-headers >= 2.6.27-0.308
BuildRequires: automake autoconf libtool pkgconfig
BuildRequires: xorg-x11-util-macros >= 1.1.5

Requires:  hwdata
Requires:  xorg-x11-server-Xorg >= 1.7.5-1
Requires:  libdrm >= 2.4.17-1
# new CS method needs newer kernel
Requires:  kernel >= 2.6.29.1-111.fc11
Obsoletes: xorg-x11-drv-avivo <= 0.0.2

%description 
X.Org X11 ati video driver.

%package firmware
Summary: ATI firmware for R600/700/800
BuildArch: noarch
ExcludeArch: s390 s390x

%description firmware
Firmware for ATI R600/R700 IRQs + R800

%prep
#%setup -q -n %{tarball}-%{gitdate} -a 2
%setup -q -n %{tarball}-%{version} -a 2
%patch2 -p1 -b .clone
%patch3 -p1 -b .uevent
%patch6 -p1 -b .bgnr
%patch10 -p1 -b .lvds
%patch13 -p1 -b .def
%patch14 -p1 -b .rn50-no-xv
%patch15 -p1 -b .rn50-clone
%patch16 -p1 -b .ppcdiff

%build
autoreconf -iv
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

%{SOURCE1} src/pcidb/ati_pciids.csv > radeon.xinf

mkdir -p $RPM_BUILD_ROOT%{_datadir}/hwdata/videoaliases
install -m 0644 radeon.xinf $RPM_BUILD_ROOT%{_datadir}/hwdata/videoaliases/

find $RPM_BUILD_ROOT -regex ".*\.la$" | xargs rm -f --

%{__mkdir_p} %{buildroot}/lib/firmware/radeon
%{__install} -p -m 0644 radeon/*.bin %{buildroot}/lib/firmware/radeon/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{driverdir}/ati_drv.so
%{driverdir}/radeon_drv.so
%{_datadir}/hwdata/videoaliases/radeon.xinf
%{moduledir}/multimedia/theatre200_drv.so
%{moduledir}/multimedia/theatre_detect_drv.so
%{moduledir}/multimedia/theatre_drv.so
%{_mandir}/man4/ati.4*
%{_mandir}/man4/radeon.4*

%files firmware
%defattr(-,root,root,-)
%doc LICENSE.radeon.firmware
/lib/firmware/radeon/*.bin

%changelog
* Fri Jun 11 2010 Dave Airlie <airlied@redhat.com> 6.13.0-6
- fix a powerpc endian + incorrect cursor pitch on rn50/power (#593949)

* Wed Jun 09 2010 Dave Airlie <airlied@redhat.com> 6.13.0-5
- fix rn50 cloning (patch from Alex Deucher @ AMD + fix 1 crtc issue) (#512023)

* Fri May 07 2010 Dave Airlie <airlied@redhat.com> 6.13.0-4
- add uevent support for hotplug monitors

* Tue Apr 27 2010 Dave Airlie <airlied@redhat.com> 6.13.0-3
- if copying the fb fails - don't display garbage (#585091)

* Fri Apr 09 2010 Dave Airlie <airlied@redhat.com> 6.13.0-2
- add r800 firmware + fix for rn50 Xv

* Thu Apr 08 2010 Dave Airlie <airlied@redhat.com> 6.13.0-1
- Upstream 6.13.0 finally released - can drop git snapshots

* Mon Mar 08 2010 Jerome Glisse <jglisse@redhat.com> 6.13.0-0.20.20100219git1b7e9a2e5
- build firmware as noarch package + add ExcludeArch to it fix (#570702)

* Thu Feb 25 2010 Dave Airlie <airlied@redhat.com> 6.13.0-0.20.20100219git1b7e9a2e5
- rebase to F-12 + zaphod fixes + clone mode server fix (#568214)

* Mon Dec 21 2009 Dave Airlie <airlied@redhat.com> 6.13.0-0.19.20091221git4b05c47ac
- rebase for latest libdrm_radeon API changes - should be final API.

* Wed Dec 02 2009 Dave Airlie <airlied@redhat.com> 6.13.0-0.18.20091201git88a50a30d
- add R600 RLC firmware for IRQ handling

* Wed Dec 02 2009 Dave Airlie <airlied@redhat.com> 6.13.0-0.17.20091201git88a50a30d
- ums displayport + bump libdrm requires for new function needed

* Tue Dec 01 2009 Dave Airlie <airlied@redhat.com> 6.13.0-0.16.20091201git88a50a30d
- fixed up multi-op support for r600s

* Fri Nov 27 2009 Dave Airlie <airlied@redhat.com> 6.13.0-0.15.20091127gita8dbf7c23
- upstream snapshot with fix for resize under shadowfb, merged multi-op

* Thu Nov 26 2009 Dave Airlie <airlied@redhat.com> 6.13.0-0.14.20091125git8b28534bc
- revert r600 multi-op for now seems to cause regression

* Wed Nov 25 2009 Dave Airlie <airlied@redhat.com> 6.13.0-0.13.20091125git8b28534bc
- rebase to upstream with r600 speed ups and r100 fixes integrated.

* Fri Nov 20 2009 Dave Airlie <airlied@redhat.com> 6.13.0-0.12.20091119git437113124
- fix r100 Xv (partly inspired by 505152), rn50 small VRAM fixes.

* Thu Nov 19 2009 Dave Airlie <airlied@redhat.com> 6.13.0-0.11.20091119git437113124
- upstream snapshot (#538561), amongst others

* Fri Oct 09 2009 Dave Airlie <airlied@redhat.com> 6.13.0-0.10.20091006git457646d73
- Don't use scratch pixmaps for rotate

* Fri Oct 09 2009 Dave Airlie <airlied@redhat.com> 6.13.0-0.9.20091006git457646d73
- reload cursors on mode switch/rotate

* Wed Oct 07 2009 Dave Airlie <airlied@redhat.com> 6.13.0-0.8.20091006git457646d73
- fix rotate (#527000)

* Tue Oct 06 2009 Dave Airlie <airlied@redhat.com> 6.13.0-0.7.20091006git457646d73
- resnapshot with VT switch fixes and mixed issue was in server which is fixed

* Wed Sep 30 2009 Dave Airlie <airlied@redhat.com> 6.13.0-0.6.20090929git7968e1fb8
- mixed appears to break r600 for some reason need to investigate disable for
  beta

* Tue Sep 29 2009 Dave Airlie <airlied@redhat.com> 6.13.0-0.5.20090929git7968e1fb8
- rebase to latest upstream for vline fixes and zaphod fixes

* Thu Sep 10 2009 Dave Airlie <airlied@redhat.com> 6.13.0-0.4.20090908git651fe5a47
- fix EXA server crasher + use mixed pixmaps for speed ups

* Tue Sep 08 2009 Dave Airlie <airlied@redhat.com> 6.13.0-0.3.20090908git651fe5a47
- New snapshot with r600 kms support

* Fri Aug 21 2009 Adam Jackson <ajax@redhat.com> 6.13.0-0.2.20090821gitb1b77a4d6
- radeon-6.13-dri2-init.patch: Fix DRI2 init.

* Fri Aug 21 2009 Dave Airlie <airlied@redhat.com> 6.13.0-0.1.20090821gitb1b77a4d6
- change versioning to git snapshot for now

* Fri Aug 21 2009 Dave Airlie <airlied@redhat.com> 6.12.2-22
- change to a git snapshot

* Tue Aug 04 2009 Dave Airlie <airlied@redhat.com> 6.12.2-21
- ati: rebase to git master - need to fixup a few patches later

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.12.2-20.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Adam Jackson <ajax@redhat.com> - 6.12.2-19.1
- ABI bump

* Thu Jun 25 2009 Dave Airlie <airlied@redhat.com> 6.12.2-19
- fix kms compat

* Mon Jun 22 2009 Dave Airlie <airlied@redhat.com> 6.12.2-18
- rebuild against xorg F12 master

* Fri Jun 19 2009 Adam Jackson <ajax@redhat.com> 6.12.2-17
- Obsoletes: xorg-x11-drv-avivo

* Tue Jun 09 2009 Dave Airlie <airlied@redhat.com> 6.12.2-16
- add KMS compat patches + dri2 fixes for running on glisse kernel

* Thu May 21 2009 Adam Jackson <ajax@redhat.com> 6.12.2-15
- Update to tip of 6.12 branch, 74cb2aba79049b792c22abf25ade3693b802b260
- Drop stuff from radeon-modeset-fixes.patch to match
- Generate radeon.xinf automatically from the CSV
- radeon-6.12.2-hax.patch: Fix cursor setup and initial framebuffer clear
  in KMS.

* Thu May 14 2009 Kyle McMartin <kyle@redhat.com> 6.12.2-14
- radeon-modeset-still-more-fixes.patch: Bump the GEM interface version to
  31 so we don't activate it... (#500801)

* Thu May 07 2009 Adam Jackson <ajax@redhat.com> 6.12.2-13
- radeon-6.12.2-lvds-default-modes.patch: Add default modes to the LVDS mode
  list if we got no EDID from the kernel.

* Wed May 06 2009 Dave Airlie <airlied@redhat.com> 6.12.2-12
- radeon-6.12.2-rs690-hack.patch - workaround rs690 hangs with firefox safely

* Tue May 05 2009 Dave Airlie <airlied@redhat.com> 6.12.2-11
- make src/mask prepare access force to GTT.

* Tue May 05 2009 Dave Airlie <airlied@redhat.com> 6.12.2-10
- radeon-modeset-fixes.patch: backport fixes from upstream for rs480 firefox gpu crash

* Tue Apr 28 2009 Dave Airlie <airlied@redhat.com> 6.12.2-9
- fix gamma code to work properly
- bump kernel requires for gamma interface not oopsing

* Tue Apr 28 2009 Dave Airlie <airlied@redhat.com> 6.12.2-8
- restrict texture coords to 0.0->1.0 explicitly.
- enable gamma now kernel is tagged

* Mon Apr 27 2009 Dave Airlie <airlied@redhat.com> 6.12.2-7
- revert rs690 fixes for now until we can research properly
- fix xv warning

* Fri Apr 24 2009 Dave Airlie <airlied@redhat.com> 6.12.2-6
- rs690: fix clamps patch so it doesn't break other cards

* Thu Apr 23 2009 Dave Airlie <airlied@redhat.com> 6.12.2-5
- rs690: fix crashing when firefox or gimp is used

* Thu Apr 16 2009 Dave Airlie <airlied@redhat.com> 6.12.2-4
- radeon-modeset.patch: fix stupid idle drawing corrupt since mmap cache

* Wed Apr 15 2009 Dave Airlie <airlied@redhat.com> 6.12.2-3
- radeon-modeset-zaphod.patch: fix zaphod under kms in theory

* Wed Apr 15 2009 Dave Airlie <airlied@redhat.com> 6.12.2-2
- radeon-modeset.patch: fix rotation + cache mmap uninit var path

* Mon Apr 13 2009 Adam Jackson <ajax@redhat.com> 6.12.2-1
- radeon 6.12.2

* Thu Apr 09 2009 Adam Jackson <ajax@redhat.com> 6.12.1-10
- radeon-6.12.1-r600-fb-size.patch: Bump fb size max on R600+ when no KMS
  so single-link dualhead stands a chance of working.

* Tue Apr 07 2009 Dave Airlie <airlied@redhat.com> 6.12.1-9
- cache mmaps for objects until remove time.

* Tue Apr 07 2009 Dave Airlie <airlied@redhat.com> 6.12.1-8
- re-enable DFS for kms

* Tue Apr 07 2009 Dave Airlie <airlied@redhat.com> 6.12.1-7
- radeon-modeset-fix-nomodeset.patch: fix no modeset paths

* Mon Apr 06 2009 Dave Airlie <airlied@redhat.com> 6.12.1-6
- kms: add config.h to get mmap working properly

* Mon Apr 06 2009 Dave Airlie <airlied@redhat.com> 6.12.1-5
- radeon-modeset.patch: break APIs;
- radeon: move to latest git fixups
- bump min kernel required

* Fri Apr 03 2009 Dave Airlie <airlied@redhat.com> 6.12.1-4
- fix up r600 xv harder

* Fri Apr 03 2009 Dave Airlie <airlied@redhat.com> 6.12.1-3
- fix up r600 xv src offsets hopefully

* Wed Apr 01 2009 Dave Airlie <airlied@redhat.com> 6.12.1-2
- attempt to fix r100/r200 xv better

* Wed Apr 01 2009 Dave Airlie <airlied@redhat.com> 6.12.1-1
- rebase to upstream + fix FUS on DRI2 + video on r100/r200 hopefully

* Mon Mar 16 2009 Dave Airlie <airlied@redhat.com> 6.12.0-2
- radeon-6.12.0-git-fixes: fixes from git upstream 

* Sat Mar 14 2009 Dave Airlie <airlied@redhat.com> 6.12.0-1
- rebase to latest -ati upstream release

* Fri Mar 13 2009 Dave Airlie <airlied@redhat.com> 6.11.0-10
- radeon-modeset.patch: merge patches into kms patch
- radeon-6.11.0-git.patch: fix suspend/resume on r600

* Thu Mar 12 2009 Adam Jackson <ajax@redhat.com> 6.11.0-9
- radeon-r600-kms-shadowfb.patch: Make R600 fall back to shadowfb whne KMS
  is enabled (as opposed to crashing).

* Thu Mar 12 2009 Dave Airlie <airlied@redhat.com> 6.11.0-8
- fix r600 GART table sizing bug

* Tue Mar 10 2009 Dave Airlie <airlied@redhat.com> 6.11.0-7
- fix r600 xv, thanks to twoerner on #radeon for testing

* Tue Mar 10 2009 Dave Airlie <airlied@redhat.com> 6.11.0-6
- master fixes for panning + enable r600 accel by default

* Sat Mar 07 2009 Dave Airlie <airlied@redhat.com> 6.11.0-5
- pull in more fixes from master

* Thu Mar 05 2009 Dave Airlie <airlied@redhat.com> 6.11.0-4
- modeset: fixup radeon Xv with latest kernel

* Tue Mar 03 2009 Dave Airlie <airlied@redhat.com> 6.11.0-3
- initial support for dynamic fb resize

* Tue Mar 03 2009 Dave Airlie <airlied@redhat.com> 6.11.0-2
- rebase to latest upstream r600 accel
- fixup VT switch on DRI2

* Fri Feb 27 2009 Dave Airlie <airlied@redhat.com> 6.11.0-1
- rebase to latest upstream
- enable R600 acceleration for EXA and Xv.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.10.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 17 2009 Dave Airlie <airlied@redhat.com> 6.10.0-3
- fix VT switch on non-kms on rawhide

* Fri Jan 30 2009 Dave Airlie <airlied@redhat.com> 6.10.0-2
- Fix corruption on rs780 hopefully

* Wed Jan 07 2009 Dave Airlie <airlied@redhat.com> 6.10.0-1
- rebase to latest upstream release

* Mon Dec 22 2008 Dave Airlie <airlied@redhat.com> 6.9.0-65
- fix rotate API

* Mon Dec 22 2008 Dave Airlie <airlied@redhat.com> 6.9.0-64
- rebuild for new API

* Sat Dec 20 2008 Dave Airlie <airlied@redhat.com> 6.9.0-63
- rebase F11 patch to upstream master + modesetting bits

* Sat Nov 01 2008 Dave Airlie <airlied@redhat.com> 6.9.0-41
- radeon-modeset.patch - hopefully speed up mozilla again

* Fri Oct 31 2008 Adam Jackson <ajax@redhat.com> 6.9.0-40
- radeon-6.9.0-dig1-hdmi.patch: Fix minor logic error.

* Fri Oct 31 2008 Adam Jackson <ajax@redhat.com> 6.9.0-39
- radeon-6.9.0-dig1-hdmi.patch: Fix initialization of DVI sinks on HDMI
  connectors for DCE3.

* Thu Oct 30 2008 Dave Airlie <airlied@redhat.com> 6.9.0-38
- don't enable DFS under kms on anything but PCIE by default.

* Thu Oct 30 2008 Dave Airlie <airlied@redhat.com> 6.9.0-37
- fix memory leak in -ati driver (#469024)

* Wed Oct 29 2008 Dave Airlie <airlied@redhat.com> 6.9.0-36
- radeon-6.9.0-add-hd3300.patch - add missing pciid (#466706)
- radeon-6.9.0-quirk-agp.patch - from Ubuntu.

* Wed Oct 29 2008 Dave Airlie <airlied@redhat.com> 6.9.0-35
- radeon-6.9.0-bgnr-enable.patch - enable bg none when kms enabled (#468879)

* Tue Oct 28 2008 Dave Airlie <airlied@redhat.com> 6.9.0-34
- remove some left over debug

* Tue Oct 28 2008 Dave Airlie <airlied@redhat.com> 6.9.0-33
- add support for wait for rendering

* Mon Oct 27 2008 Dave Airlie <airlied@redhat.com> 6.9.0-32
- move to CS2 mechanism - using chunks to avoid multiple relocations
- add kernel requires about 2.6.27.4-52 for new CS mechanism

* Thu Oct 23 2008 Dave Airlie <airlied@redhat.com> 6.9.0-31
- limit VRAM usage in driver - not perfect but a good start

* Thu Oct 23 2008 Dave Airlie <airlied@redhat.com> 6.9.0-30
- fix some bad memory allocations

* Tue Oct 21 2008 Dave Airlie <airlied@redhat.com> 6.9.0-29
- fix most obvious glyph corruption issues in modesetting mode

* Sun Oct 19 2008 Dave Airlie <airlied@redhat.com> 6.9.0-28
- fix set tex offset for non modesetting cases

* Wed Oct 15 2008 Dave Airlie <airlied@redhat.com> 6.9.0-27
- modeset - radeon add support for basic r100/r200 EXA
- modeset - add Download from screen accel.
- radeon-6.9.0-to-git.patch : fix 30" monitor

* Mon Oct 13 2008 Dave Airlie <airlied@redhat.com> 6.9.0-26
- radeon-modeset.patch - fix nexuiz mode switch - remove unused reuse code

* Fri Oct 10 2008 Dave Airlie <airlied@redhat.com> 6.9.0-25
- fix rotation
- make output names compatible with non-kms

* Fri Oct 10 2008 Dave Airlie <airlied@redhat.com> 6.9.0-24
- radeon-modeset.patch - fix silly debugging fallback.

* Fri Oct 10 2008 Dave Airlie <airlied@redhat.com> 6.9.0-23
- rebase to upstream master
- radeon-6.9.0-lvds-mapping.patch - merged upstream
- copy-fb-contents.patch merged into modesetting tree.

* Wed Oct 08 2008 Adam Jackson <ajax@redhat.com> 6.9.0-22
- radeon-6.9.0-lvds-mapping.patch: Fix connector mapping on LVDS.

* Wed Oct 01 2008 Dave Airlie <airlied@redhat.com> 6.9.0-21
- rebase for latest fixes and new libdrm

* Mon Sep 29 2008 Dave Airlie <airlied@redhat.com> 6.9.0-20
- fix collision with copy fb contents patch

* Mon Sep 29 2008 Dave Airlie <airlied@redhat.com> 6.9.0-19
- fix textured video + merge otaylor fix into exa fixes patch

* Sat Sep 27 2008 Dave Airlie <airlied@redhat.com> 6.9.0-18
- fix fb contents patch
- EXA speedup from otaylor.

* Fri Sep 26 2008 Dave Airlie <airlied@redhat.com> 6.9.0-17
- exa offset fixes for changes in X server

* Fri Sep 26 2008 Dave Airlie <airlied@redhat.com> 6.9.0-16
- rebase to a later tree - still not fully up to git master
- add some fixes to the resize stuff - not fully done

* Fri Sep 19 2008 Kristian Høgsberg <krh@redhat.com> - 6.9.0-15
- Add copy-fb-contents.patch to initialize the root window contents
  with the fbdev contents for slick startup.

* Thu Sep 11 2008 Adam Jackson <ajax@redhat.com> 6.9.0-14
- radeon-6.9.0-panel-size-sanity.patch: Panels smaller than 800x480 are
  highly implausible, disable them if we find them.  If you have one,
  you can force it with Option "PanelSize".

* Thu Sep 11 2008 Soren Sandmann <sandmann@redhat.com> 6.9.0-13
- Remove the fb size hack since there is a fix in the server now.
- Unfortunately, the driver prevents this fix from working by applying 
  its own heuristics. Remove those.

* Wed Sep 10 2008 Adam Jackson <ajax@redhat.com> 6.9.0-12
- Do the fb size hack a differently bad way.

* Tue Sep  9 2008 Kristian Høgsberg <krh@redhat.com> 6.9.0-11
- Restore CFLAGS after testing for DRM_MODE in radeon-modeset.patch.

* Mon Sep 08 2008 Adam Jackson <ajax@redhat.com> 6.9.0-10
- radeon-6.9.0-fb-size.patch: Yet more lame heuristics to preallocate a
  usable framebuffer for laptops. (#458864)

* Fri Sep 05 2008 Dave Airlie <airlied@redhat.com> 6.9.0-9
- add fix for pipe register emits on r300

* Fri Sep 05 2008 Dave Airlie <airlied@redhat.com> 6.9.0-8
- fix suspend/resume support - needs new pinning API

* Wed Aug 27 2008 Dave Airlie <airlied@redhat.com> 6.9.0-7
- fix bug in modesetting to make 3D work again

* Tue Aug 26 2008 Dave Airlie <airlied@redhat.com> 6.9.0-6
- update modesetting/memory manager support

* Fri Aug 15 2008 Dave Airlie <airlied@redhat.com> 6.9.0-5
- Add a perl script to generate the radeon.xinf from the actual PCI IDs the driver supports.
- not build integrated yet though
- update pciids

* Fri Aug 15 2008 Dave Airlie <airlied@redhat.com> 6.9.0-4
- fix bugs in modesetting and bring PLL fixes in from master

* Thu Aug 14 2008 Dave Airlie <airlied@redhat.com> 6.9.0-3
- bring back modesetting

* Mon Aug 11 2008 Adam Jackson <ajax@redhat.com> 6.9.0-2
- Rebuild without modesetting since libdrm lost the API.  It'll be back soon,
  I'm sure.

* Sun Aug 10 2008 Adam Jackson <ajax@redhat.com> 6.9.0-1
- Move to 6.9.0, now that the r128 and mach64 drivers are split out.
- Add git fixes since 6.9.0.
- Rebase the modesetting patch onto git master.

* Wed Aug 06 2008 Dave Airlie <airlied@redhat.com> 6.8.0-21
- bunch of fixes to modesetting code + remove debugging.

* Fri Aug 01 2008 Dave Airlie <airlied@redhat.com> 6.8.0-20
- DDX modesetting code

* Wed Jul 30 2008 Dave Airlie <airlied@redhat.com> 6.8.0-19
- Update to latest upstream release + fixes

* Thu Jun 26 2008 Dave Airlie <airlied@redhat.com> 6.8.0-18
- update to latest git 6.8.192 beta

* Wed May 28 2008 Dave Airlie <airlied@redhat.com> 6.8.0-17
- fix multiple VT switch issues on r600 cards
- assorted upstream goodness

* Sat May 24 2008 Dave Airlie <airlied@redhat.com> 6.8.0-16
- Fix PLL on r600 LVDS (#444542)
- update to other upstream fixes

* Mon May 12 2008 Dave Airlie <airlied@redhat.com> 6.8.0-15
- The RS482 sucks - same pci id, mobile and non-mobile parts.

* Mon May 12 2008 Dave Airlie <airlied@redhat.com> 6.8.0-14
- add initial cloning support for RN50 (#439879)

* Wed May 07 2008 Dave Airlie <airlied@redhat.com> 6.8.0-13
- more upstream fixes for EXA accel + zaphod mode

* Thu Apr 24 2008 Dave Airlie <airlied@redhat.com> 6.8.0-12
- not so much faster as kill my Apple MAC DDC - next time do this upstream first

* Thu Apr 24 2008 Dave Airlie <airlied@redhat.com> 6.8.0-11
- fix r128 bios size issue (#439022)

* Sun Apr 06 2008 Dave Airlie <airlied@redhat.com> 6.8.0-10
- attempt to fix VT switch and X restart hangs

* Wed Apr 02 2008 Dave Airlie <airlied@redhat.com> 6.8.0-9
- attempt to fix dualhead and rotation at the same time.

* Mon Mar 31 2008 Dave Airlie <airlied@redhat.com> 6.8.0-8
- Hopefully fix quirks not applying on radeon LVDS (#435126)
- quirk connector table from (#428515)
- fix rotate on r500 cards

* Sun Mar 30 2008 Dave Airlie <airlied@redhat.com> 6.8.0-7
- Major upstream fixes backported - render accel, xv etc.
- This is done with a separate patch as upstream has split mach64/r128 already

* Fri Mar 28 2008 Adam Jackson <ajax@redhat.com> 6.8.0-6
- radeon.xinf: :1,$s/radeon_tp/radeon/

* Wed Mar 26 2008 Dave Airlie <airlied@redhat.com> 6.8.0-5
- Fix mach64 on ia64 with 16k pagesize (#438947)

* Tue Mar 11 2008 Adam Jackson <ajax@redhat.com> 6.8.0-4
- r500-dual-link-love.patch: Make R300+ max CRTC size guess big enough
  for a 30" monitor.

* Mon Mar 03 2008 Dave Airlie <airlied@redhat.com> 6.8.0-3
- rebuild for upstream ABI breakage

* Tue Feb 26 2008 Dave Airlie <airlied@redhat.com> 6.8.0-2
- rebase to upstream 6.8.0 release + git fixes

* Tue Feb 19 2008 Dave Airlie <airlied@redhat.com> 6.8.0-1
- rebase to upstream 6.8.0 release.

* Mon Feb 18 2008 Dave Airlie <airlied@redhat.com> 6.7.197-3
- rebase to upstream git master - lots of r600 fixes

* Fri Feb 08 2008 Dave Airlie <airlied@redhat.com> 6.7.197-2
- rebase to upstream git master - add rv67x ids

* Mon Feb 04 2008 Dave Airlie <airlied@redhat.com> 6.7.197-1
- rebase to upstream git master
- add r5xx and r6xx pci ids to xinf

* Thu Jan 17 2008 Dave Airlie <airlied@redhat.com> 6.7.196-7
- fix up IGPs from upstream fix.

* Wed Jan 09 2008 Adam Jackson <ajax@redhat.com> 6.7.196-6
- Rebuild for new server ABI.

* Wed Jan 02 2008 Adam Jackson <ajax@redhat.com> 6.7.196-5
- r128-6.7.196-pciaccess.patch: Fix some preprocessor dumbness.

* Wed Jan 02 2008 Adam Jackson <ajax@redhat.com> 6.7.196-4
- r128-6.7.196-pciaccess.patch: Port r128 to libpciaccess.

* Wed Dec 19 2007 Dave Airlie <airlied@redhat.com> 6.7.196-3
- radeon-git-upstream-fixes.patch - update for latest git master
- radeon-6.7.196-atombios-support.patch - update for r500/r600

* Mon Dec 17 2007 Adam Jackson <ajax@redhat.com> 6.7.196-2
- *-6.7.196-alloca.patch: Fix ALLOCATE_LOCAL failures.

* Wed Nov 14 2007 Adam Jackson <ajax@redhat.com> 6.7.196-1
- xf86-video-ati 6.7.196

* Tue Nov 13 2007 Adam Jackson <ajax@redhat.com> 6.7.195-5
- Require xserver 1.4.99.1

* Thu Nov 08 2007 Adam Jackson <ajax@redhat.com> 6.7.195-4
- radeon-6.7.195-faster-ddc.patch: Speed up X startup by assuming the
  monitor doesn't need a dead chicken waved over it to get DDC.

* Tue Oct 16 2007 Dave Airlie <airlied@redhat.com> 6.7.195-3
- upstream fixes including previous patches + attempted mac detection

* Tue Oct 09 2007 Adam Jackson <ajax@redhat.com> 6.7.195-2
- DDC and LVDS patches from git.

* Sat Oct 06 2007 Adam Jackson <ajax@redhat.com> 6.7.195-1
- xf86-video-ati 6.7.195

* Fri Oct 5 2007 Dave Airlie <airlied@redhat.com> 6.7.194-3
- radeon-6.7.194-upstream-fixes - Upstream LVDS fixes
  improve chances of working on more panels.

* Fri Sep 28 2007 Dave Airlie <airlied@redhat.com> 6.7.194-2
- radeon-6.7.194-disable-rc410-dri.patch - Disable DRI on
  RC410 by default as it seems to need some more work.

* Mon Sep 24 2007 Dave Airlie <airlied@redhat.com> 6.7.194-1
- xf86-video-ati 6.7.194

* Thu Sep 20 2007 Dave Airlie <airlied@redhat.com> 6.7.193-1
- xf86-video-ati 6.7.193

* Mon Aug 27 2007 Adam Jackson <ajax@redhat.com> 6.7.192-1
- xf86-video-ati 6.7.192

* Mon Aug 27 2007 Dave Airlie <airlied@redhat.com> 6.7.191-2
- radeon-6.7.191-git-master.patch - upgrade to git head
  f36720377737210c985b196d9a988efdd767f1c7

* Tue Aug 23 2007 Dave Airlie <airlied@redhat.com> 6.7.191-1
- xf86-video-ati 6.7.191. - Add a pre-release of radeon randr code
  This will break old zaphod mode further than the current 6.6.193
  driver, and will probably break mergedfb configs, however it will
  work with randr-1.2 properly and is the more supported codebase going
  forward.

* Tue Aug 21 2007 Adam Jackson <ajax@redhat.com> - 6.6.193-3
- Rebuild for build id

* Wed Aug 08 2007 Dave Airlie <airlied@redhat.com> 6.6.193-2
- xf86-video-ati 6.6.193. - remove dotclock workaround for now
  It causes crashes bug 251051

* Sat Aug 04 2007 Dave Airlie <airlied@redhat.com> 6.6.193-1
- xf86-video-ati 6.6.193.

* Wed Jun 27 2007 Adam Jackson <ajax@redhat.com> 6.6.192-1
- xf86-video-ati 6.6.192.

* Tue Jun 19 2007 Adam Jackson <ajax@redhat.com> 6.6.3-4
- radeon-6.6.3-renderaccel-buglet.patch: Fix OpenOffice font corruption
  when RenderAccel is disabled. (#244675)

* Mon Jun 18 2007 Adam Jackson <ajax@redhat.com> 6.6.3-3
- Update Requires and BuildRequires.  Disown the module directories.  Add
  Requires: hwdata.

* Thu Feb 15 2007 Adam Jackson <ajax@redhat.com> 6.6.3-2
- ExclusiveArch -> ExcludeArch

* Tue Nov 7 2006 Adam Jackson <ajackson@redhat.com> 6.6.3-1.fc7
- Update to 6.6.3.

* Mon Oct 2 2006 Adam Jackson <ajackson@redhat.com> 6.6.2-4
- ati-prefer-radeon-then-r128.patch: When loading through the 'ati' wrapper,
  prefer radeon to rage128 to mach{64,32,16,8,4,2,1}. 
- r128-fp-dpms.patch: Hook up DPMS for Rage128 DFPs. (#197436)
- radeon-6.6.2-dac-fix.patch: Even though we turn DACs on for probing, don't
  turn them off.  Fixes black screen of death post-rhgb.  (#208610)
- radeon-6.6.2-pmac-bios.patch: Be more suspicious of ROMs before interpreting
  their content.  (#208694)
- radeon-6.6.2-usefbdev-patch.patch: Use the framebuffer stride from fbdev,
  instead of making up numbers.  (#208694)

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 6.6.2-3
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Thu Sep 21 2006 Adam Jackson <ajackson@redhat.com> 6.6.2-2.fc6
- radeon-6.6.2-dac-fix.patch: Backport 25fa71... from git.  Turn on the DAC
  before doing CRT connection probe, otherwise we might incorrectly detect
  a CRT where there isn't one. (#202240 and others)

* Tue Aug 29 2006 Adam Jackson <ajackson@redhat.com> 6.6.2-1.fc6
- Update to 6.6.2 from upstream:
  - Mach64 stability and correctness fixes
  - Mach64 EXA support.
  - Misc bugfixes for radeon.

* Thu Aug 24 2006 Adam Jackson <ajackson@redhat.com> 6.6.1-11.fc6
- radeon-6.6.1-use-mtdriver.patch: Only flag modes with M_T_PREFERRED if
  the EDID blocks says to.

* Fri Aug 18 2006 Adam Jackson <ajackson@redhat.com> 6.6.1-10.fc6
- radeon-6.6.1-use-mtdriver.patch: Use new M_T_DRIVER mode type for mode
  synthesis.
- Bump Requires to match.

* Fri Aug 18 2006 Adam Jackson <ajackson@redhat.com> 6.6.1-9.fc6
- mach64-cpio-for-ia64.patch: Enable CPIO for mach64 on ia64. (#203017)

* Thu Aug 10 2006 Adam Jackson <ajackson@redhat.com> 6.6.1-8.fc6
- radeon-6.6.1-xpress-200.patch: Also disable DRI on xpress200, known broken.

* Wed Aug  2 2006 Adam Jackson <ajackson@redhat.com> 6.6.1-7.fc6
- Make sure DRI and Render accel are disabled on RN50.

* Sat Jul 29 2006 Kristian Høgsberg <krh@redhat.com> 6.6.1-6.fc5.aiglx
- Build for fc5 aiglx repo.

* Thu Jul 27 2006 Adam Jackson <ajackson@redhat.com> 6.6.1-6.fc6
- Updated radeon.xinf: comments, a handful of new devices.

* Mon Jul 24 2006 Mike A. Harris <mharris@redhat.com> 6.6.1-5.fc6
- Added r128-missing-xf86ForceHWCursor-symbol-bug168753.patch to fix (#168753)
- Add {?dist} tag to Release field

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> 6.6.1-4.1
- rebuild

* Wed Jun 28 2006 Mike A. Harris <mharris@@redhat.com> 6.6.1-4
- Added "BuildRequires: xorg-x11-server-sdk >= 1.1.0-12" to fix the same
  problem at build time as were added in 6.6.1-2 to fix it at runtime.

* Tue Jun 27 2006 Kristian Høgsberg <krh@redhat.com> 6.6.1-3
- Bump release for FC5 aiglx build.

* Mon Jun 26 2006 Adam Jackson <ajackson@redhat.com> 6.6.1-2
- Filter the EDID mode list by the monitor's reported pixel clock.  Bump
  the BuildReq to a server that provides the necessary ABI field.

* Sat Jun 17 2006 Mike A. Harris <mharris@redhat.com> 6.6.1-1
- Updated xorg-x11-drv-ati to version 6.6.1 update release for X11R7.1
- Drop db-root-visual.patch, as it is included in 6.6.1
- Enable DRI support for sparc/sparc64 builds.

* Fri Jun  9 2006 Kristian Høgsberg <krh@redhat.com> 6.6.0-7
- Committed db-root-visual.patch and reenabled.

* Thu Jun  8 2006 Mike A. Harris <mharris@@redhat.com> 6.6.0-6
- Disable db-root-visual.patch, because the file wasn't committed to CVS.

* Thu Jun  8 2006 Kristian Høgsberg <krh@redhat.com> 6.6.0-5
- Bump for rawhide build.

* Thu Jun  8 2006 Kristian Høgsberg <krh@redhat.com> 6.6.0-4
- Add db-root-visual.patch to make root visual double buffered.

* Tue May 23 2006 Adam Jackson <ajackson@redhat.com> 6.6.0-3
- Rebuild for 7.1 ABI fix.

* Tue Apr 11 2006 Kristian Høgsberg <krh@redhat.com> 6.6.0-2
- Bump for fc5-bling build.

* Sun Apr  9 2006 Adam Jackson <ajackson@redhat.com> 6.6.0-1
- Update to 6.6.0 from 7.1RC1.

* Tue Apr  4 2006 Kristian Høgsberg <krh@redhat.com> 6.5.7.3-4.cvs20060404
- Update to CVS snapshot from 20060404.

* Wed Mar 22 2006 Kristian Høgsberg <krh@redhat.com> 6.5.7.3-4.cvs20060322
- Update to CVS snapshot of 20060322.
- Drop xorg-x11-drv-ati-6.5.7.3-radeon-metamodes-SEGV-fix.patch.

* Tue Feb 21 2006 Mike A. Harris <mharris@redhat.com> 6.5.7.3-4
- Added xorg-x11-drv-ati-6.5.7.3-radeon-metamodes-SEGV-fix.patch from CVS HEAD.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 6.5.7.3-3.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 6.5.7.3-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Sun Feb 05 2006 Mike A. Harris <mharris@redhat.com> 6.5.7.3-3
- Updated radeon.xinf to be up to date with the xf86PciInfo.h from the Xorg
  X server 1.0.1-1 source.  This should account for all supported Radeon
  models now modulo errors/omissions.

* Thu Feb 02 2006 Mike A. Harris <mharris@redhat.com> 6.5.7.3-2
- Added r128.xinf and radeon.xinf videoalias files to fix bug (#174101).
- Added "BuildRequires: libdrm-devel >= 2.0-1" to fix bug (#178613)

* Wed Jan 18 2006 Mike A. Harris <mharris@redhat.com> 6.5.7.3-1
- Updated xorg-x11-drv-ati to version 6.5.7.3 from X11R7.0
- Added ati.xinf videoalias file for hardware autodetection.

* Tue Dec 20 2005 Mike A. Harris <mharris@redhat.com> 6.5.7.2-1
- Updated xorg-x11-drv-ati to version 6.5.7.2 from X11R7 RC4
- Removed 'x' suffix from manpage dirs to match RC4 upstream.

* Wed Nov 16 2005 Mike A. Harris <mharris@redhat.com> 6.5.7-1
- Updated xorg-x11-drv-ati to version 6.5.7 from X11R7 RC2

* Fri Nov 4 2005 Mike A. Harris <mharris@redhat.com> 6.5.6.1-1
- Updated xorg-x11-drv-ati to version 6.5.6.1 from X11R7 RC1
- Fix *.la file removal.
- Add "BuildRequires: mesa-libGL-devel >= 6.4-4 for DRI builds"

* Mon Oct 3 2005 Mike A. Harris <mharris@redhat.com> 6.5.6-1
- Update BuildRoot to use Fedora Packaging Guidelines.
- Deglob file manifest.
- Use _smp_mflags with make, to speed up SMP builds.
- Add "alpha sparc sparc64" to ExclusiveArch

* Fri Sep 2 2005 Mike A. Harris <mharris@redhat.com> 6.5.6-0
- Initial spec file for ati video driver generated automatically
  by my xorg-driverspecgen script.
