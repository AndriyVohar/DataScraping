<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\Models\DepartmentItem;
use App\Models\FacultyItem;

class DepartmentItemController extends Controller
{
    public function index()
    {
        $DepartmentItems = DepartmentItem::orderBy('id', 'desc')->with('faculty')->get();
        return response()->json($DepartmentItems, 200);
    }
    public function store(Request $request)
    {
        $request->validate([
            'name' => 'required',
            'url' => 'required',
            'faculty' => 'required'
        ]);
        $requestTask = $request->all();
        $faculty = FacultyItem::where('name', $requestTask['faculty'])->first();
        $requestTask['faculty_id'] = $faculty->id;
        $DepartmentItem = DepartmentItem::create($requestTask);
        return response()->json($DepartmentItem, 201);
    }

    public function show($id)
    {
        $DepartmentItem = DepartmentItem::with('faculty')->findOrFail($id);
        return $DepartmentItem;
    }
    public function update(Request $request, DepartmentItem $DepartmentItem)
    {
        $request->validate([
            'name'=>'required',
            'url'=>'required',
        ]);
        $DepartmentItem->update($request->all());
        return $DepartmentItem;
    }
    public function destroy($id)
    {
        $DepartmentItem = DepartmentItem::findOrFail($id);
        $DepartmentItem->delete();
        return response(200);
    }
}
