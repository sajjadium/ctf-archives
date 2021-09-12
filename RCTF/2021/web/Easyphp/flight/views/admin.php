
<h3>File List:</h3>
<script>
</script>
<div class="bg-light border rounded-3" style="white-space: pre-line">
    <?php
        $dir = pathinfo($data?$data:".",PATHINFO_DIRNAME);
        foreach(scandir($dir) as $v){
            echo "<a href=\"/admin?data=$dir/$v\">$v</a><br />";
        }
    ?>
</div>
<?php if ($data) { ?><h3><?= $data . ":" ?></h3>
    <div class="bg-light border rounded-3"><code style="white-space: pre-line"><?php echo file_get_contents($data); ?></code></div><?php } ?>