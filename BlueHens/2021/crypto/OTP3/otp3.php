7ac19a94522b60ea531929c3ba0ae72ccbd2dcc2e726b45ba42024b7be8eb8f8d3e2cb5f8d351c541439cda662b2d7ba416f7b87bfad326382feb54ce48db013c3b1f9c16da6d5ec53e3beedd9e018e2b4375df13b32d8091f775ec2f908abccc0314e5f936ece00f9155a90a51f7713b11c814a25b809ef32a1a7e15170de3a8b02229a4687286462e81ddd9b0fa2d15fa6d82872fe97e0509c79f178879ac80b43f0a27e230a0a4ef27bfa3a4f5bcc53cc91d1bda935332e469c109508edce976d61175c7bb75f52ecf046d360d29c1268866ad1ea93c5b4b319ba05259efdefc0c6a6fcd7281fc917167e65c284a538c5e883c1190001110728383a61371d213b7a371a20672e1665173b64396717312564300b2531292b1278202e3aaec6c04482ab0d56663dd5175d6a37093b0565868b74eb767dc37d6f7818f67caebaaa374904230a9028cb67bcf8ae261238af2528dce63f73a4b0c7934536a6fd1b3d4007cc8d3d59ceeacebb25200ca9701e86983946d0483399f975cd1265b1405c2182ab9ba0cba2b0aa970813f8b43cba3a028b2d96c5c6cf27a68eeb2bc34243379fecf3e8b1f53f9e49672074fb30356a436c621dddb869889ede61cb4a5dd719e816485c86620c1c7c20f25936098dae1aec385667f4847d66c88b8e563476fd530824c1bb17f221cad9c1def925a15ea42d3cbda29faef4d4e2cc508b250355012fd0b162b7dcba5a716095a7b63c6e85e6b04dfc97b81ec5b1eec77aabd1ed53e7baedc5f618feb53c55ec3024dc1a1d774ad0fa07a9cadd2945438f68c30ee5075b9ba31370@@7ac19a8b5e2c77ec5d0e21c1b103e424d0dfdac9ff2cb55fae212da6a597b8ead5f9dd47863004500320cab769b6c8a64f767d8daba02a728dfdbd4df893bd04c3b1fcd76baad3f04ff0a9fbc3e709ffae2553ed3922c61c1d714bd7f91cbbd0dd204f558e78c30ee5045c91b2086113b6179d5a33ba19e832aba2eb5661cb3c9d0523864290207874fd1fd0860aa9db52bacf3073f98cfd518e7eff6f989acf165ef0bd77200b035ce265e7265b40d442de86d9a1a935332a438d109f0ae3c488656916516cba5f55e5ff59c466d68a0f758068d9fd8ac6afb408a80c2894e6efdcd2a4e6cb2c18d416006f61ca87bf37cef883d2130d0011073533207a3d0b3b26742c1a207b2c11750c316728611e323c762b1e3e24323b137d31333fb9cbc25286a80c5c762ad1075e6a29012118638e8b65f37267d867757e0ae870a5b3ba36541e270c8c2fc66cabe3a1251a3cae332ac0fb336ba6acc98e5936b8e1123e5c06ca9c355ac1eedbbe3f3e0ca478139193224ac54f3499e271c41471a84058369ba581a0cbada0a19f0001e2a82ea1231f8d219acad5de30b890e639c353493594f1f6e2a8e72b9f4c683a7ef520306c40767f0ed4a27e8098c168d44c4cd603f815454381720b0b6a36f2592e0f86bf04e82e4d6de6957878cc8c925f2770eb510d2dceb615fd36cbdaddd8e228ae45ad2820bda39ebcf5d6f0c14d943e0548133dd7b369b6c9a14f6d7a91bdb53a7483fcb14cf28bae07c4baeec16eabddfd48eaadfad3e315f7b22b5efe232eda1d02715ddff20daecbdc27485b8973d406e6045b86b3126100ac17854d2cbf05fd29a7a6e54d
<?php
  $raw = file_get_contents("../../quotes.txt");
  //concatenated quotes stripped of non alphabetical characters 
  //all caps for each character
  //one quote set per newline
  //each around 600 bytes i.e. /[A-Z]{596,604}/
  $quotes = explode("\n",$raw);
  $plaintexti = array_rand($quotes);
  $plaintext = $quotes[$plaintexti];
  $plaintext2i = array_rand($quotes);
  $plaintext2 = $quotes[$plaintext2i];
  
  function pad_string($string, $length) {
    $string_length = strlen($string);
    if ($length <= $string_length){
        return $string;
    }
    $prefl = mt_rand(1,$length - $string_length);
    return random_bytes($prefl).$string.random_bytes($length - $string_length - $prefl);
  }
  
  //For these 3 problems I'll only change these 2 lines:
  $flag = trim(file_get_contents("../../flag3.txt"));
  $key = pad_string($flag, mt_rand(250,550)); 

  function xor_string($string, $key) {
    for($i = 0; $i < strlen($string); $i++) 
      $string[$i] = ($string[$i] ^ $key[$i % strlen($key)]);
    return $string;
  }
  
  $ciphertext1 = xor_string($plaintext, $key);
  echo bin2hex($ciphertext1);
  echo "@@";
  $ciphertext2 = xor_string($plaintext2, $key);
  echo bin2hex($ciphertext2);
  
  echo highlight_file(__FILE__, true);
?>
