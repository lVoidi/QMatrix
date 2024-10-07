from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile import bar, layout, qtile, widget, hook
from libqtile.backend.wayland import InputConfig
from libqtile.lazy import lazy
import subprocess

# Colors

bar_font = "FiraCode Nerd Font"

crypto_color = "#8899b9"
clock_color = "#7689af"
layout_color = "#697ea8"
systray_color = "#6076a2"
button_colors = "#506997"

# crypto_color = "#506997"
# clock_color = "#6076a2"
# layout_color = "#697ea8"
# systray_color = "#7689af"
# button_colors = "#8899b9"

main_color = "#4a6496"
dim_color = "#455c89"

mod = "mod4"
terminal = "kitty"
web_browser = "firefox"
file_browser = "pcmanfm"
run_cmd = "rofi -show drun"
screenshooter = "flameshot gui"
calendar = "gnome-calendar"
monitor = "htop"
hwmonitor = f"{terminal} -e {monitor}"
audio_control = "pavucontrol"
wireshark = f"{terminal} -e sudo tshark"
discord = "discord"
telegram = "telegram-desktop"
# crypto = '{terminal} -e cointop&'
crypto = f"{web_browser} https://coinmarketcap.com/currencies/sui/"

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key(
        [mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key(
        [mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"
    ),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.window.toggle_minimize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod], "Right", lazy.screen.next_group(), desc="Next workspace"),
    Key([mod], "Left", lazy.screen.prev_group(), desc="Previous workspace"),
    Key([mod], "Up", lazy.next_layout(), desc="Next layout"),
    Key([mod], "Down", lazy.prev_layout(), desc="Previous layout"),
    Key(
        [mod],
        "-",
        lazy.spawn("amixer sset Master 5%-"),
        desc="Lower Volume by 5%",
    ),
    Key(
        [mod],
        "=",
        lazy.spawn("amixer sset Master 5%+"),
        desc="Raise Volume by 5%",
    ),
    Key(
        [],
        "XF86AudioMute",
        lazy.spawn("amixer sset Master 1+ toggle"),
        desc="Mute/Unmute Volume",
    ),
    Key(
        [],
        "XF86AudioPlay",
        lazy.spawn("playerctl play-pause"),
        desc="Play/Pause player",
    ),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next"), desc="Skip to next"),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous"), desc="Skip to previous"),
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key(
        [mod, "shift"],
        "Return",
        lazy.window.toggle_floating(),
        desc="Toggle floating on the focused window",
    ),
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn(run_cmd), desc="Spawn a command using a prompt widget"),
    Key([mod], "e", lazy.spawn(file_browser), desc="Spawn file browser"),
    Key([mod], "w", lazy.spawn(web_browser), desc="Spawn web browser"),
    Key([mod], "v", lazy.spawn(audio_control), desc="Spawn audio controller"),
    Key([mod], "d", lazy.spawn(discord), desc="Spawn audio controller"),
    Key([mod], "t", lazy.spawn(telegram), desc="Spawn audio controller"),
    Key([mod], "c", lazy.spawn(wireshark), desc="Spawn audio controller"),
    Key([], "Print", lazy.spawn(screenshooter), desc="Spawn screenshooter"),
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


groups = [Group(i) for i in "αβδθλσφψω"]

for index, group in enumerate(groups):
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                str(index + 1),
                lazy.group[group.name].toscreen(),
                desc="Switch to group {}".format(group.name),
            ),
            Key(
                [mod, "shift"],
                str(index + 1),
                lazy.window.togroup(group.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(group.name),
            ),
        ]
    )

layouts = [
    layout.Columns(
        border_focus_stack=["00ff00", "00ff00"],
        border_focus=main_color,
        border_normal=dim_color,
        border_width=5,
        margin=10,
    ),
    layout.Floating(
        border_focus=main_color,
        border_normal=dim_color,
        float_rules=[
            *layout.Floating.default_float_rules,
            Match(wm_class="confirmreset"),  # gitk
            Match(wm_class="makebranch"),  # gitk
            Match(wm_class="maketag"),  # gitk
            Match(wm_class="ssh-askpass"),  # ssh-askpass
            Match(title="branchdialog"),  # gitk
            Match(title="pinentry"),  # GPG key password entry
        ],
    ),
]

widget_defaults = dict(
    font=bar_font,
    fontsize=12,
    foreground="#000000",
    padding=5,
)
extension_defaults = widget_defaults.copy()

widgets = [
    widget.TextBox(
        " ",
        foreground=main_color,
        fontsize=35,
        mouse_callbacks={"Button1": lazy.spawn(run_cmd)},
    ),
    widget.GroupBox(
        highlight_method="line",
        active=main_color,
        font="Hack Nerd Font",
        this_current_screen_border="#ffffff",
        fontsize=25,
        fontshadow="#003300",
        # background="#008800",
        margin=3,
        rounded=False,
    ),
    widget.Spacer(bar.STRETCH),
    widget.TextBox(
        "CPU",
        fontsize=15,
        foreground=main_color,
        mouse_callbacks={"Button1": lazy.spawn(hwmonitor)},
    ),
    widget.CPUGraph(
        frequency=0.05,
        graph_color=main_color,
        fill_color=main_color,
        mouse_callbacks={"Button1": lazy.spawn(hwmonitor)},
        border_color=main_color,
    ),
    widget.TextBox(
        "MEM",
        fontsize=15,
        mouse_callbacks={"Button1": lazy.spawn(hwmonitor)},
        foreground=main_color,
    ),
    widget.MemoryGraph(
        frequency=0.05,
        mouse_callbacks={"Button1": lazy.spawn(hwmonitor)},
        graph_color=main_color,
        fill_color=main_color,
        border_color=main_color,
    ),
    widget.TextBox(
        "NET",
        fontsize=15,
        mouse_callbacks={"Button1": lazy.spawn(wireshark)},
        foreground=main_color,
    ),
    widget.NetGraph(
        frequency=0.05,
        mouse_callbacks={"Button1": lazy.spawn(wireshark)},
        graph_color=main_color,
        fill_color=main_color,
        border_color=main_color,
    ),
    widget.Spacer(bar.STRETCH),
    widget.TextBox(
        "󰒢",
        foreground=crypto_color,
        fontsize=60,
        mouse_callbacks={"Button1": lazy.spawn(crypto)},
    ),
    widget.CryptoTicker(
        background=crypto_color,
        fontsize=20,
        crypto="SUI",
        mouse_callbacks={"Button1": lazy.spawn(crypto)},
        format="$SUI   {amount:.4f}$",
    ),
    widget.Clock(
        format=" %I:%M %p",
        background=clock_color,
        fontsize=20,
        mouse_callbacks={"Button1": lazy.spawn(calendar)},
    ),
    widget.CurrentLayout(
        background=layout_color,
        foreground="#000000",
        fontsize=20,
        fmt="|{}|",
    ),
    widget.Battery(background=layout_color, format="{percent:1.2%} 󰁹", fontsize=20),
    widget.TextBox(
        " ",
        foreground="#000000",
        background=button_colors,
        fontsize=30,
        mouse_callbacks={"Button1": lazy.spawn("systemctl poweroff")},
    ),
    widget.TextBox(
        " ",
        foreground="#000000",
        background=button_colors,
        fontsize=30,
        mouse_callbacks={"Button1": lazy.spawn("systemctl reboot")},
    ),
    # 
    widget.TextBox(
        " ",
        foreground="#000000",
        background=button_colors,
        fontsize=30,
        mouse_callbacks={"Button1": lazy.spawn("systemctl suspend")},
    ),
]

screens = [
    Screen(
        wallpaper="~/.config/qtile/wallpaper.png",
        wallpaper_mode="fill",
        bottom=bar.Bar(
            widgets,
            35,
            # border_width=[1, 0, 5, 0],  # Draw top and bottom borders
            # border_color=["aaffaa", "000000", "77ff77", "000000"]  # Borders are magenta
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []
floating_layout = layout.Floating(
    border_focus=main_color,
    border_normal=dim_color,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ],
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True
wl_input_rules = {
    "2:8:AlpsPS/2 ALPS GlidePoint": InputConfig(
        tap=True, kb_repeat_delay=400, accel_profile="flat", natural_scroll=True
    )
}
wl_xcursor_theme = None
wl_xcursor_size = 24
wmname = "DELTA"


@hook.subscribe.startup_once
def on_init():
    subprocess.Popen("/usr/lib/policykit-1-gnome/polkit-gnome-authentication-agent-1")
    subprocess.run(["setxkbmap", "us", "-variant", "altgr-intl"])
