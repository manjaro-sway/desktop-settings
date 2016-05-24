last_job_id(1) -- Get the id of the last job to be started
==========================================================

## SYNOPSIS

last_job_id<br>

## USAGE

```fish
if set -l job_id (last_job_id)
    printf "The last job to be started: %%%i\n" $job_id
end
```
