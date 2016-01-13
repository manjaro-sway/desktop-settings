#!/usr/bin/perl
# fbmenugen - schema file

=for comment

    item:	add an item inside the menu	{item => ["command", "label", "icon"]},
    cat:	add a category inside the menu	{cat => ["name", "label", "icon"]},
    sep:	horizontal line separator	{sep => undef}, {sep => "label"},
    raw:	any valid Fluxbox menu entry	{raw => q(...)},
    begin_cat:	begin of a category		{begin_cat => ["name", "icon"]},
    end_cat:	end of a category		{end_cat => undef},
    fbmenugen:	generic menu settings		{fbmenugen => ["label", "icon"]},
    fluxbox:	the default Fluxbox config menu	{fluxbox => ["label", "icon"]},
    exit:	default "Exit" action		{exit => ["label", "icon"]},

=cut

# NOTE:
#    * Keys and values are case sensitive. Keep all keys lowercase.
#    * ICON can be a either a direct path to an icon or a valid icon name
#    * Category names are case insensitive. (X-XFCE and x_xfce are equivalent)
#
#						LABEL			ICON
#  {begin_cat =>				['My category',		'cat-icon']},
#	... some items ...
#  {end_cat => undef},

require "$ENV{HOME}/.config/fbmenugen/config.pl";

our $SCHEMA = [
{item =>	['sudo calamares',		'Install Manjaro (Calamares)','calamares']},
{item =>	['sudo thus',			'Install Manjaro (Thus)','thus']},
{item =>	['sudo lxterminal -e setup',	'Install Manjaro (CLI)',]},

{sep => 'undef'},

{item =>	['lxterminal',			'Terminal',		'terminal']},
{item =>	['pcmanfm',			'File Manager',		'file-manager']},
{item =>	['gksu pcmanfm',		'Root File Manager',	'root-file-manager']},
{cat =>		['network',			'Internet',		'applications-internet']},
{cat =>		['office',			'Office',		'applications-office']},
{cat =>		['graphics',			'Graphics',		'applications-graphics']},
{cat =>		['audiovideo',			'Multimedia',		'applications-multimedia']},
{cat =>		['education',			'Education',		'applications-science']},
{cat =>		['game',			'Games',		'applications-games']},
{begin_cat =>					['Tools',		]},
  {cat =>	['utility',			'Accessories',		'applications-utilities']},
  {begin_cat =>					['Screenshot',		]},
    {item => 	['fb-screenshot -d',		'full screen',		]},
    {item => 	['fb-screenshot -w',		'active window',	]},
    {item => 	['fb-screenshot -s',		'select area',		]},
  {end_cat => undef},
  {cat =>	['system',			'System',		'applications-system']},
  {cat =>	['settings',			'Settings',		'applications-accessories']},
{end_cat => undef},
{cat =>		['other',			'Other',		'applications-other']},
# {cat =>	['development',			'Development',		'applications-development']},
# {cat =>	['qt',				'QT Applications',	'qtlogo']},
# {cat =>	['gtk',				'GTK Applications',	'gnome-applications']},
# {cat =>	['x_xfce',			'XFCE Applications',	'applications-other']},
# {cat =>	['gnome',			'GNOME Applications',	'gnome-applications']},
# {cat =>	['consoleonly',			'CLI Applications',	'applications-utilities']},

{sep => 'undef'},

{begin_cat =>					['Customization',	]},
  {item =>	['lxappearance',		'Appearance',		]},
  {item =>	['plank --preferences',		'Dock',			]},
  {item =>	['gksu lightdm-gtk-greeter-settings','LightDM Greeter',	]},
  {item =>	['xfce4-notifyd-config',	'Notifications',	]},
  {item =>	['nitrogen',			'Wallpaper',		]},
{end_cat => undef},
{begin_cat =>					['Fluxbox Settings',	]},
  {raw => q([config] (Behaviour))},
  {raw => q([workspaces] (Workspace List))},
  {regenerate =>				['Regenerate menu',     'gtk-refresh']},
 
{sep => 'undef'},

  {raw => q([commanddialog] (Command line))},
  {raw => q([reconfig] (Reload config))},
  {raw => q([restart] (Restart))},
{end_cat => undef},

# Time Settings (GUI)
# TimeSet (CLI)
# menu_de neu!!

{sep => 'undef'},

{item =>	['oblogout',			'Exit',			'shutdown/restart']}
]
