<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('staff_items', function (Blueprint $table) {
            $table->id();
            $table->string('head_of_department', 70);
            $table->string('address', 70);
            $table->string('phone', 20);
            $table->string('email', 40);
            $table->foreignId('department_id')
                ->constrained('department_items')
                ->onUpdate('cascade')
                ->onDelete('cascade');
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('staff_items');
    }
};
