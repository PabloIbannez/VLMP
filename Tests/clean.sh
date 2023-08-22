for f in */*Test.py; do
		echo $(dirname $f)
		cd $(dirname $f)
		./clean.sh
		cd ..
done
