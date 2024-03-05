<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class DepartmentItem extends Model
{
    use HasFactory;
    protected $fillable=[
        'name',
        'url',
        'faculty_id',
    ];
    public function faculty(){
        return $this->belongsTo(FacultyItem::class,'faculty_id');
    }
    public function staff(){
        return $this->hasMany(StaffItem::class,'department_id');
    }
}
