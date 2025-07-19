<?php
header('Access-Control-Allow-Origin: *');
header('Content-Type: application/json');

if (!isset($_GET['q'])) {
    echo json_encode(['erro' => 'Nome não informado']);
    exit;
}

$nome = urlencode($_GET['q']);
$pagina = isset($_GET['p']) ? intval($_GET['p']) : 1;
$url = "https://www.portaldatransparencia.gov.br/pessoa-fisica/busca/resultado?termo=$nome&pagina=$pagina&tamanhoPagina=10&t=wdUJNlyLKulB1HjVJkn0&tokenRecaptcha=03AFcWeA4DXPwC9M1vCB5CO9KM1PqzNxwp2gNs80thmXkCJLg9w9PzDwxJv14wggAUnNAWamNIMRKxSq3a5_mRzciHUo1Lq5_-ICGBofvCfeHEhQOxJwP5e-ys9FXEmiJk9jF4LIGilEujQga0SDwN-WU7IJ0aWlKB32SAxceX9iz9kS49_ZhSC2oFaWv9CTTr9JaobNyNczk3gs-gOTfCtJf1wF-j69zM5AMfAwbPorXoYETIZ7sG8qYtcIemdPKvPJc78HqbM3DS4HUm3GhqM6ZNGqY5e8kW8-U3_rGUXBI3CfXrb9IKOS-vBI2J-xvQpz3KhNWJ3k2v2-9sP0MJJ3nqkgIoB5JQS14EK1plXeaQF2Ez2YFXH03ZfUbVF4-253NAon3xsAr_8lfaM-APpuabMFJ3cF1LihK3lEo9ebkrCs7du8M95XNhwqtRCJ9AueyUTAxvKmBMsM6cs8vMap7BQvPUkPyDqc-s6bOjfp8z11ahS_sVqZ9XLMEHdJriC-eGP3rXc5wrYOU3H9dG6xS8ykm1YCBxp4tJ85vyVWqXBmxo620uIhZea_6fc11FRXkXxfwKZzVMl5P-OQvqaqjHX94k486jeHP910SAbNIkeKqEqN3SCIj-XPkHLqh0-nkdr5Hl1sYi_xNzCfCJEiNTwtjwIjQ8vTidojbIfLHbRI3jzEYLS7XZIJusJClYJm1zZnT5ePRZn14Grse2aIzGzZoyM0ANOQbtV3WZm538bGkrUl5NFWYw4pF5yYx0jf-8fHzwMQgsAMMdQcuS2SdUXOtsOQOLae71Jlxe945kxllejVW-hoi0_dsd_ebKzSD84vTIpCRRwt5Qrn-8aJXwMFZOg9Z-ToGnWlFPSo0Cpp7N613aKK2K8ozdNH5SF3MpvZM7aj-bGU2mMGrWjmjo85OaNXF04RCGqmLS58r5JNx3mp6crhzZbqcbh0qntEanK6ATdyug";

$resposta = @file_get_contents($url);

if ($resposta) {
    echo $resposta;
} else {
    echo json_encode(['erro' => 'Erro ao buscar na API']);
}
?>