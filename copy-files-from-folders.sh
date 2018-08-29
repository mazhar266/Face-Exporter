for d in */; do
	cd "$d"
	echo Copying from $d
	cp -R -f * ../../folder_name/
	cd ..
done

