<!DOCTYPE html>
<html>
<head>
    <title>Y******Dev's Sorting Algorithm Timer</title>
    <style>
        table {
            border-collapse: collapse;
        }
        th, td {
            padding: 8px;
            border: 1px solid black;
        }
    </style>
</head>
<body>
    <h1>Y******Dev's Sorting Algorithm Timer</h1>
    <form action="index.php" method="post">
        <label for="filename">File to shuffle:</label>
        <select name="filename" id="filename">
            <option value="words_shuffled.txt">words_shuffled.txt</option>
            <option value="alice_in_wonderland.txt">alice_in_wonderland.txt</option>
            <option value="quotes.txt">quotes.txt</option>
        </select>
        <input type="submit" value="Submit">
    </form>
    <?php 
        function bubbleSort($arr) {
            $n = count($arr);
            for ($i = 0; $i < $n; $i++) {
                for ($j = 0; $j < $n - $i - 1; $j++) {
                    if ($arr[$j] > $arr[$j + 1]) {
                        $temp = $arr[$j];
                        $arr[$j] = $arr[$j + 1];
                        $arr[$j + 1] = $temp;
                    }
                }
            }
            return $arr;
        }
        function selectionSort($arr) {
            $n = count($arr);
            for ($i = 0; $i < $n - 1; $i++) {
                $min = $i;
                for ($j = $i + 1; $j < $n; $j++) {
                    if ($arr[$j] < $arr[$min]) {
                        $min = $j;
                    }
                }
                $temp = $arr[$i];
                $arr[$i] = $arr[$min];
                $arr[$min] = $temp;
            }
            return $arr;
        }
        function insertionSort($arr) {
            $n = count($arr);
            for ($i = 1; $i < $n; $i++) {
                $key = $arr[$i];
                $j = $i - 1;
                while ($j >= 0 && $arr[$j] > $key) {
                    $arr[$j + 1] = $arr[$j];
                    $j--;
                }
                $arr[$j + 1] = $key;
            }
            return $arr;
        }
        function mergeSort($arr) {
            $n = count($arr);
            if ($n > 1) {
                $mid = floor($n / 2);
                $left = array_slice($arr, 0, $mid);
                $right = array_slice($arr, $mid);
                $left = mergeSort($left);
                $right = mergeSort($right);
                $arr = merge($left, $right);
            }
            return $arr;
        }
        function merge($left, $right) {
            $result = array();
            while (count($left) > 0 && count($right) > 0) {
                if ($left[0] <= $right[0]) {
                    array_push($result, array_shift($left));
                } else {
                    array_push($result, array_shift($right));
                }
            }
            while (count($left) > 0) {
                array_push($result, array_shift($left));
            }
            while (count($right) > 0) {
                array_push($result, array_shift($right));
            }
            return $result;
        }
        function quickSort($arr) {
            $n = count($arr);
            if ($n <= 1) {
                return $arr;
            }
            $pivot = $arr[0];
            $left = array();
            $right = array();
            for ($i = 1; $i < $n; $i++) {
                if ($arr[$i] < $pivot) {
                    array_push($left, $arr[$i]);
                } else {
                    array_push($right, $arr[$i]);
                }
            }
            $left = quickSort($left);
            $right = quickSort($right);
            return array_merge($left, array($pivot), $right);
        }
        function heapSort($arr) {
            $n = count($arr);
            for ($i = floor($n / 2) - 1; $i >= 0; $i--) {
                heapify($arr, $n, $i);
            }
            for ($i = $n - 1; $i >= 0; $i--) {
                $temp = $arr[0];
                $arr[0] = $arr[$i];
                $arr[$i] = $temp;
                heapify($arr, $i, 0);
            }
            return $arr;
        }
        function heapify(&$arr, $n, $i) {
            $largest = $i;
            $left = 2 * $i + 1;
            $right = 2 * $i + 2;
            if ($left < $n && $arr[$left] > $arr[$largest]) {
                $largest = $left;
            }
            if ($right < $n && $arr[$right] > $arr[$largest]) {
                $largest = $right;
            }
            if ($largest != $i) {
                $temp = $arr[$i];
                $arr[$i] = $arr[$largest];
                $arr[$largest] = $temp;
                heapify($arr, $n, $largest);
            }
        }
        if (isset($_POST['filename'])) {
            $filename = $_POST['filename'];
            $contents = file_get_contents($filename);
            $arr = explode("\n", $contents);

            // god i wish there was an easier way to do this
            $arr_copy = $arr;
            $start = microtime(true);
            sort($arr_copy);
            $end = microtime(true);
            $sort_time = $end - $start;

            $arr_copy = $arr;
            $start = microtime(true);
            $arr_copy = bubbleSort($arr_copy);
            $end = microtime(true);
            $bubble_sort_time = $end - $start;

            $arr_copy = $arr;
            $start = microtime(true);
            $arr_copy = selectionSort($arr_copy);
            $end = microtime(true);
            $selection_sort_time = $end - $start;

            $arr_copy = $arr;
            $start = microtime(true);
            $arr_copy = insertionSort($arr_copy);
            $end = microtime(true);
            $insertion_sort_time = $end - $start;

            $arr_copy = $arr;
            $start = microtime(true);
            $arr_copy = mergeSort($arr_copy);
            $end = microtime(true);
            $merge_sort_time = $end - $start;

            $arr_copy = $arr;
            $start = microtime(true);
            $arr_copy = quickSort($arr_copy);
            $end = microtime(true);
            $quick_sort_time = $end - $start;

            $arr_copy = $arr;
            $start = microtime(true);
            $arr_copy = heapSort($arr_copy);
            $end = microtime(true);
            $heap_sort_time = $end - $start;
            
            $start = microtime(true);
            exec("sort " . escapeshellcmd($filename));
            $end = microtime(true);
            $sort_utility_time = $end - $start;

            echo "<table>";
            echo "<tr><th>Algorithm</th><th>Time</th></tr>";
            echo "<tr><td>PHP sort</td><td>$sort_time</td></tr>";
            echo "<tr><td>Bubble sort</td><td>$bubble_sort_time</td></tr>";
            echo "<tr><td>Selection sort</td><td>$selection_sort_time</td></tr>";
            echo "<tr><td>Insertion sort</td><td>$insertion_sort_time</td></tr>";
            echo "<tr><td>Merge sort</td><td>$merge_sort_time</td></tr>";
            echo "<tr><td>Quick sort</td><td>$quick_sort_time</td></tr>";
            echo "<tr><td>Heap sort</td><td>$heap_sort_time</td></tr>";
            echo "<tr><td>GNU sort</td><td>$sort_utility_time</td></tr>";
            echo "</table>";
        }
    ?>
</body>
</html>