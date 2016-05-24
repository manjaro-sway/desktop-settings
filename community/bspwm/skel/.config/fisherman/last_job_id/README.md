[![Build Status][travis-badge]][travis-link]
[![Slack Room][slack-badge]][slack-link]

# last_job_id

Get the id of one or more existing jobs

## Install

With [fisherman]

```
fisher last_job_id
```

## Usage

```fish
if set -l i (last_job_id --last)
    printf "Most recent job: %%%i\n" $i
end
```

[travis-link]: https://travis-ci.org/fisherman/last_job_id
[travis-badge]: https://img.shields.io/travis/fisherman/last_job_id.svg
[slack-link]: https://fisherman-wharf.herokuapp.com/
[slack-badge]: https://fisherman-wharf.herokuapp.com/badge.svg
[fisherman]: https://github.com/fisherman/fisherman
