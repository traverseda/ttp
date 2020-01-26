# Time Tracker Plus

`ttp`, a time tracker inspired by `utt`. There are some some changes I wanted to
do to utt that would have required some pretty big changes in how it worked, so
unfortunatly I decided a rewrite would be easier.

ttp us a python time tracker that differs in one major way, you tell the time
tracker what you've done *after* you've already done it.

start tracking time with `ttp start`, then when you've finished a task add it
with `ttp add updated my resume`. You can edit your log with `ttp edit`.

`ttp project someproject` changes what project you're logging to.

## Instalation

```
pip install pipx --user
pipx install time-tracker-plus
```

Optionally enable bash's tab-completion by adding this to your `~/.bashrc` file.

`eval "$(_TTP_COMPLETE=source ttp)"`
