function await -d "Wait for background jobs"
	if test -z "$argv"
        set argv (last_job_id)
    end

    set -l spinners "$await_spinners"
    set -l interval "$await_interval"

    if test -z "$spinners"
        set spinners ⠋ ⠙ ⠹ ⠸ ⠼ ⠴ ⠦ ⠧ ⠇ ⠏
    end

    if test -z "$interval"
        set interval 0.05
    end

    while true
        for spinner in $spinners
            printf "  $spinner  \r" > /dev/stderr
            sleep "$interval"
        end

        set -l currently_active_jobs (last_job_id)

        if test -z "$currently_active_jobs"
            break
        end

        set -l has_jobs

        for i in $argv
            if builtin contains -- $i $currently_active_jobs
                set has_jobs "*"
                break
            end
        end

        if test -z "$has_jobs"
            break
        end
    end
end
