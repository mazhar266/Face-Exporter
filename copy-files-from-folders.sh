for d in */; do
	cd "$d"
	echo Copying from $d
	cp * ../../folder_name/ -R -f
	cd ..
done

