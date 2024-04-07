<?php

namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;
use Illuminate\Support\Str;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\Repository>
 */
class RepositoryFactory extends Factory
{
    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition(): array
    {
        $gh_name = \Faker\Factory::create()->regexify('^[a-z0-9]{7}$');
        $repo_name = \Faker\Factory::create()->regexify('^[a-z0-9]{5}$');
        return [
            'id' => Str::uuid(),
            'name' => $repo_name,
            'description' => fake()->randomElement([null, fake()->sentence()]),
            'license' => fake()->randomElement([null, 'MIT', 'Apache']),
            'open_issues' => fake()->numberBetween(0, 30),
            'gh_user_name' => $gh_name,
            'fork' => fake()->boolean(10), // true の確率。
        ];
    }
}
