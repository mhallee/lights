#!/bin/bash

if [ ! -d "$Results" ]; then
  	echo "   Making \" Results\" folder..."
	mkdir Results
fi

echo "Removing CRFL characters from all files in pwd..."
for file in *.cd
do
	if test -f "$file"
	then
		echo "   $file"
		#cat $file | tr -d "\r" > Results/$file
	fi
done
echo "Process complete. Check \"Results\" folder for new files."
sleep 2
