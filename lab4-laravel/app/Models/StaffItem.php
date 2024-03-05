<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class StaffItem extends Model
{
    use HasFactory;
    protected $fillable=[
        'head_of_department',
        'address',
        'phone',
        'email',
        'department_id',
    ];
    public function department(){
        return $this->belongsTo(DepartmentItem::class,'department_id');
    }
}
