#!/bin/env sh
pip3 list --outdated | grep -v '^\\-e' | cut -d = -f 1 |awk 'NR>2{print $1}' > outdated_packages.txt

while IFS= read -r pkg_name
do
  echo "pkg_name_to_update: $pkg_name";
  pip install --upgrade "$pkg_name"

done < outdated_packages.txt
