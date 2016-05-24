function fish_title
  echo "$PWD | $_" | sed "s|$HOME|~|g"
end