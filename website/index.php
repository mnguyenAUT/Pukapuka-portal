<center>
<?php
if (isset($_GET['u'])) {
  $tkiURL = $_GET['u'];;
}
if (isset($_GET['url'])) {
  $tkiURL = $_GET['url'];;
}

$arr = array("RRPP" => "Ready-to-Read-Phonics-Plus","RRCW" => "Ready-to-Read-Colour-Wheel","JJ" => "Junior-Journal","SJ" => "School-Journal");

$tkiURL = strtr($tkiURL,$arr);

?>

<?php
//https://instructionalseries.tki.org.nz/Instructional-Series/
$content = file_get_contents($tkiURL);
// True because $a is empty
if (empty($content)) {
  $content = file_get_contents("https://instructionalseries.tki.org.nz/Instructional-Series/".$tkiURL);
}

$doc = new DOMDocument();
$doc->loadHTML($content);
$xpath = new DOMXPath($doc);

//MP3 file
$src = $xpath->evaluate("string(//source/@src)");
$mp3File = $src;
echo "<br/>";

//PDF file
$src = $xpath->evaluate("string(//a[@class='pdf-ico']/@href)");
$pdfFile = $src;
if ($pdfFile == "") {
	$src = $xpath->evaluate("string(//a[@class='tsm-ico']/@href)");
	$pdfFile = $src;
}

//JPG file
$src = $xpath->evaluate("string(//div[@class='frame']//img/@src)");
$jpgFile = $src;

?>

<p>
<img src="https://instructionalseries.tki.org.nz<?php echo $jpgFile; ?>" height="75%">
</p>
<p>
<a href="read.php?url=https://instructionalseries.tki.org.nz<?php echo $pdfFile; ?>" target="<?php if (empty($mp3File)) echo '_parent'; else echo '_blank'; ?>">
<!--
MP3: https://instructionalseries.tki.org.nz<?php echo $mp3File; ?>
-->
<audio controls autoplay>
  <source src="https://instructionalseries.tki.org.nz<?php echo $mp3File; ?>" type="audio/mpeg">
  Your browser does not support the audio element.
</audio>
</a>
</p>
</center>
<iframe src="read.php?url=https://instructionalseries.tki.org.nz<?php echo $pdfFile; ?>" style="display:none"></iframe>
<?php
/*if (empty($mp3File)) 
{
	//header("Location: read.php?url=https://instructionalseries.tki.org.nz");
	header('Location: http://www.example.com/');
	exit;
}
*/
?>


