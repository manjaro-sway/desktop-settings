[![Build Status][travis-badge]][travis-link]
[![Slack Room][slack-badge]][slack-link]

# Await

Wait for background jobs.

## Install

With [fisherman]

```
fisher await
```

## Usage

Wait until all existing jobs have finished.

```fish
await
```

Wait until the given jobs are finished.

```fish
set -l id_list

for cmd in $commands
    fish -c "$cmd" &
    set id_list $id_list (last_job_id -l)
end

await $id_list
```

Customize spinners.

```fish
set await_spinners ◢ ◣ ◤ ◥
```

Customize interval between spinners.

```fish
set await_interval 0.1
```

[travis-link]: https://travis-ci.org/fisherman/await
[travis-badge]: https://img.shields.io/travis/fisherman/await.svg
[slack-link]: https://fisherman-wharf.herokuapp.com/
[slack-badge]: https://fisherman-wharf.herokuapp.com/badge.svg
[fisherman]: https://github.com/fisherman/fisherman
