<?php

namespace Database\Seeders;

use App\Models\Repository;
use App\Models\User;
// use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;

class FeatureTestRepositorySeeder extends Seeder
{
    /**
     * Seed the application's database.
     */
    public function run(): void
    {
        Repository::factory()->count(20)->create();
    }
}
