function fish_prompt
  test $status -ne 0;
    and set -l colors 600 900 c00
    or set -l colors 666 aaa 2B9

  set -l pwd (pwd | sed "s|$HOME|~|g")
  set -l base (basename "$pwd")

  set -l expr "s|~|"(fst)"~"(off)"|g; \
               s|/|"(snd)"/"(off)"|g;  \
               s|"$base"|"(fst)$base(off)" |g"

  echo -n (echo "$pwd" | sed -e $expr)(off)

  for color in $colors
    echo -n (set_color $color)">"
  end

  echo -n " "
end
