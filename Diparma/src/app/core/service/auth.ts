import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { LoginResponse } from '../../models/login-response.model';
import { UsuarioCreate, UsuarioResponse, EnderecoCreate } from '../../models/usuario.model';

@Injectable({
  providedIn: 'root'
})
export class Auth {
  private apiUrl = 'http://127.0.0.1:8000/'; // 🧠 Ajuste conforme sua API

  constructor(private http: HttpClient) {}

  login(email: string, senha: string): Observable<LoginResponse> {
    return this.http.post<LoginResponse>(`${this.apiUrl}usuarios/login`, { email, senha });
  }

  createUsuario(payload: UsuarioCreate): Observable<UsuarioResponse> {
    return this.http.post<UsuarioResponse>(`${this.http}usuarios`, payload);
  }

  createEndereco(payload: EnderecoCreate): Observable<any> {
    return this.http.post<any>(`${this.http}enderecos`, payload);
  }
}
