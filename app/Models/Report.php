<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Report extends Model
{
    use HasFactory;
    
    /**
     * Os atributos que podem ser atribuídos em massa.
     */
    protected $fillable = [
        'ticker',
        'report_draft_ai',
        'status',
        'report_final_human', 
        'human_notes',      
    ];
}