<?php

namespace App\Solutions;

use Spatie\Ignition\Contracts\RunnableSolution;

class FlagSolution implements RunnableSolution
{
  public function getSolutionTitle(): string
  {
    return 'Flag';
  }

  public function getSolutionDescription(): string
  {
    return 'Get the flag';
  }

  public function getDocumentationLinks(): array
  {
    return [];
  }


  public function getSolutionActionDescription(): string
  {
    return 'Get the flag';
  }

  public function getRunButtonText(): string
  {
    return 'Press here to get the flag';
  }

  public function run(array $parameters = []): void
  {
    throw 'PTM{THIS_IS_THE_FLAG}';
  }

  public function getRunParameters(): array
  {
    return ['url'];
  }

  public function isRunnable(): bool
  {
    return true;
  }
}
