<?php
namespace Drupal\flag\Controller;
use Drupal\Core\Controller\ControllerBase;

class FlagController extends ControllerBase
{
    public function index()
    {
        return array(
            '#type' => 'markup',
            '#markup' => $this->t('Flag: FAKE{real_flag_is_on_the_challenge_instance}!'),);
    }
}