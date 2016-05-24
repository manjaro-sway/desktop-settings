test "$TESTNAME - Get the id of the last job to be started"
    (
        sleep 0.2&
        set -l jobs_id (jobs -l | cut -d\t -f1)
        echo "$jobs_id"

    ) = (last_job_id)
end

test "$TESTNAME - Set status to 1 if there are no jobs"
    1 = (

        while true
            set -l has_jobs (jobs)
            if test -z "$has_jobs"
                break
            end
        end

        last_job_id
        echo $status

        )
end
