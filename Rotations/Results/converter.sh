#bin/bash

if [! -d "$Results"]; then
	echo "Making \"Results\" folder..."
	mkdir Results
fi

echo "Converting files..."

for file in *.cd
	if [-f "$file"]; then
		echo "  -- $file"
		cat $file | tr -d "\r" > Results/$file
	fi	
done

echo "Process complete.  Files deposited in \"Results\" folder.
