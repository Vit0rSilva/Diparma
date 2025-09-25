import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Prato } from '../../models/prato.model'; 
import { Observable } from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class Api {
  apiUrl: string = "http://localhost:3001/";

  constructor(private http: HttpClient){}

  //Observable - ele fica obserrvando quando os dados da api chegar
  getPratos(): Observable<Prato[]>{
    return this.http.get<Prato[]>(this.apiUrl + 'pratos');
  }

  /*salvar(categoria: Categoria) : Observable<Categoria>{
    return this.http.post<Categoria>(this.apiUrl, categoria);
  }*/

}
