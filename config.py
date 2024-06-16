from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
import subprocess
from libqtile.utils import guess_terminal

mod = "mod4"
terminal = "alacritty"
web_browser = "firefox-esr"
file_browser = "nautilus -w"
run_cmd = "rofi -show drun"
screenshooter = "flameshot gui"
calendar = "gnome-calendar"
monitor = "htop"
hwmonitor = f"{terminal} -e {monitor}"
audio_control = "pavucontrol"

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
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod], "Right", lazy.screen.next_group(), desc="Next workspace"),
    Key([mod], "Left", lazy.screen.prev_group(), desc="Next workspace"),
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
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn(run_cmd), desc="Spawn a command using a prompt widget"),
    Key([mod], "e", lazy.spawn(file_browser), desc="Spawn file browser"),
    Key([mod], "w", lazy.spawn(web_browser), desc="Spawn web browser"),
    Key([mod], "v", lazy.spawn(audio_control), desc="Spawn audio controller"),
    Key([], "Print", lazy.spawn(screenshooter), desc="Spawn screenshooter")
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
        border_focus="#00ff00",
        border_normal="#009900",
        border_width=5,
        margin=10,
    ),
]

widget_defaults = dict(
    font="Hack Nerd Font",
    fontsize=12,
    foreground="#000000",
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        wallpaper="/home/void/.config/qtile/wallpaper.png",
        wallpaper_mode='fill',
        bottom=bar.Bar(
            [
                widget.TextBox(
                    " ",
                    foreground="#00ff00",
                    fontsize=30,
                    mouse_callbacks={
                        "Button1": lazy.spawn(run_cmd)
                    }
                ),
                widget.GroupBox(
                    highlight_method='line',
                    active="#00ff00",
                    font="Hack Nerd Font",
                    this_current_screen_border="#ffffff",
                    fontsize=15,
                    fontshadow="#003300",
                    #background="#008800",
                    margin=3,
                    rounded=False
                ),
                widget.Spacer(bar.STRETCH),
                widget.TextBox(
                    "CPU",
                    foreground="#00ff00",
                    mouse_callbacks={"Button1": lazy.spawn(hwmonitor)},
                ),
                widget.CPUGraph(
                    frequency=0.05,
                    graph_color="#00ff00",
                    fill_color="#00ff00",
                    mouse_callbacks={"Button1": lazy.spawn(hwmonitor)},
                    border_color="#00ff00"
                ),
                widget.TextBox(
                    "MEM",
                    mouse_callbacks={"Button1": lazy.spawn(hwmonitor)},
                    foreground="#00ff00"
                ),
                widget.MemoryGraph(
                    frequency=0.05,
                    mouse_callbacks={"Button1": lazy.spawn(hwmonitor)},
                    graph_color="#00ff00",
                    fill_color="#00ff00",
                    border_color="#00ff00"
                ),
                widget.TextBox(
                    "NET",
                    mouse_callbacks={"Button1": lazy.spawn(hwmonitor)},
                    foreground="#00ff00"
                ),
                widget.NetGraph(
                    frequency=0.05,
                    mouse_callbacks={"Button1": lazy.spawn(hwmonitor)},
                    graph_color="#00ff00",
                    fill_color="#00ff00",
                    border_color="#00ff00"
                ),
                widget.Spacer(bar.STRETCH),
                widget.Clock(
                    format="%I:%M %p",
                    background="#00ff00",
                    fontsize=20,
                    mouse_callbacks={"Button1": lazy.spawn(calendar)}
                ),
            ],
            30,
            #border_width=[1, 0, 5, 0],  # Draw top and bottom borders
            #border_color=["aaffaa", "000000", "77ff77", "000000"]  # Borders are magenta
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True
wl_input_rules = None
wl_xcursor_theme = None
wl_xcursor_size = 24
wmname = "DELTA"

@hook.subscribe.startup
def on_init():
    subprocess.run(["setxkbmap", "us", "-variant", "altgr-intl"])
