import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Usuario } from '../../models/usuario.model';
import { Endereco } from '../../models/endereco.model';

@Injectable({
  providedIn: 'root'
})
export class User {
  apiUrl: string = "http://localhost:3001/";

  constructor(private http: HttpClient){}

  getUsuarios(id: number): Observable<Usuario[]>{
    return this.http.get<Usuario[]>(this.apiUrl + 'usuarios?id='+id);
  }

  getEndereco(id: number): Observable<Endereco[]>{
    return this.http.get<Endereco[]>(this.apiUrl + 'endereco?id=' + id);
  }
}
