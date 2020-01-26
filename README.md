# Time Tracker Plus

`ttp`, a time tracker inspired by `utt`.

ttp is a python time tracker where you tell the time
tracker what you've done *after* you've already done it. Like writing a git
commit message.

start tracking time with `ttp start`, then when you've finished a task add it
with `ttp add updated my resume`. You can edit your log with `ttp edit`.

`ttp project someproject` changes what project you're logging to.

`ttp report` shows a report of your current tasks. Help is wanted for this, as
we need more template options. Uses jinja2 for templating.

## Instalation

```
pip install pipx --user
pipx install time-tracker-plus
```

Optionally enable bash's tab-completion by adding this to your `~/.bashrc` file.

`eval "$(_TTP_COMPLETE=source ttp)"`

## Example report

You can write new reports using jinja2. Personally I use this to generate
invoices for clients, directly from my hours.

```markdown
# default
## Monday, January 20th, 2020 to Sunday, January 26th, 2020

 *  1.00h worked on time tracker
 *  4.00h worked on time tracker2
 * 22.00h worked on time tracker3
 *  1.88h worked on time tracker overnight

28.88 hours worked total
```
