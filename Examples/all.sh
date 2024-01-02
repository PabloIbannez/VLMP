for f in */*Test.py; do
		echo "Running $f"
		cd $(dirname $f)
		# Run the test. If error, echo the error and exit.
		python $(basename $f) || { echo "Error in $f"; exit 1; }
		./clean.sh
		cd ..
done
