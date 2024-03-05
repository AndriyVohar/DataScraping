<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class FacultyItem extends Model
{
    use HasFactory;
    protected $fillable=[
        'name',
        'url'
    ];
    public function department(){
        return $this->hasMany(DepartmentItem::class,'faculty_id');
    }
    
}
