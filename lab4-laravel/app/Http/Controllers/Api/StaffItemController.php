<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\Models\DepartmentItem;
use App\Models\StaffItem;
class StaffItemController extends Controller
{
    public function index()
    {
        $StaffItems = StaffItem::orderBy('id', 'desc')->with('department')->get();
        return response()->json($StaffItems, 200);
    }
    public function store(Request $request)
    {
        $request->validate([
            'head_of_department' => 'required',
            'address' => 'required',
            'email' => 'required',
            'phone' => 'required',
            'department' => 'required'
        ]);
        $requestTask = $request->all();
        $department = DepartmentItem::where('name', $requestTask['department'])->first();
        $requestTask['department_id'] = $department->id;
        $StaffItem = StaffItem::create($requestTask);
        return response()->json($StaffItem, 201);
    }

    public function show($id)
    {
        $StaffItem = StaffItem::with('department')->findOrFail($id);
        return $StaffItem;
    }
    public function update(Request $request, StaffItem $StaffItem)
    {
        $request->validate([
            'name'=>'required',
            'url'=>'required',
        ]);
        $StaffItem->update($request->all());
        return $StaffItem;
    }
    public function destroy($id)
    {
        $StaffItem = StaffItem::findOrFail($id);
        $StaffItem->delete();
        return response(200);
    }
}
