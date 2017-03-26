SUBDIRS = icons

desktopdir = $(datadir)/applications
desktop_in_files = org.gnome.parlatype.desktop.in
desktop_DATA = $(desktop_in_files:.desktop.in=.desktop)
@INTLTOOL_DESKTOP_RULE@

install-desktop-database: install-desktopDATA
	update-desktop-database $(DESTDIR)$(desktopdir)

gsettings_SCHEMAS = org.gnome.parlatype.gschema.xml
@GSETTINGS_RULES@

appdatadir = $(datadir)/appdata
appdata_in_files = org.gnome.parlatype.appdata.xml.in
appdata_DATA = $(appdata_in_files:.xml.in=.xml)
@INTLTOOL_XML_RULE@

check-local: $(desktop_DATA) $(appdata_DATA)
	$(DESKTOP_FILE_VALIDATE) $(desktop_DATA)
	$(APPDATA_VALIDATE) validate-relax --nonet $(appdata_DATA)

CLEANFILES = \
	$(appdata_DATA)		\
	$(desktop_DATA)

EXTRA_DIST = \
	org.gnome.parlatype.gschema.xml	\
	$(desktop_in_files)		\
	$(appdata_in_files)