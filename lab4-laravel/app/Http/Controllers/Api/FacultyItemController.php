<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\Models\FacultyItem;

class FacultyItemController extends Controller
{
    public function index()
    {
        $FacultyItems = FacultyItem::orderBy('id', 'desc')->get();
        return response()->json($FacultyItems, 200);
    }
    public function store(Request $request)
    {
        $request->validate([
            'name' => 'required',
            'url' => 'required',
        ]);
        // $requestTask = $request->all();
        // $worker = Role::where('role', $requestTask['worker'])->first();
        // $requestTask['worker_id'] = $worker->id;
        $FacultyItem = FacultyItem::create($request->all());
        return response()->json($FacultyItem, 201);
    }

    public function show($id)
    {
        $FacultyItem = FacultyItem::findOrFail($id);
        return $FacultyItem;
    }
    public function update(Request $request, FacultyItem $FacultyItem)
    {
        $request->validate([
            'name'=>'required',
            'url'=>'required'
        ]);
        $FacultyItem->update($request->all());
        return $FacultyItem;
    }
    public function destroy($id)
    {
        $FacultyItem = FacultyItem::findOrFail($id);
        $FacultyItem->delete();
        return response(200);
    }
}
