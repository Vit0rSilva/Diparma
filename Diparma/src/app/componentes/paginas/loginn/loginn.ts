import { Component } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { Auth } from '../../../core/service/auth';

@Component({
  selector: 'app-loginn',
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './loginn.html',
  styleUrl: './loginn.scss'
})
export class Loginn {
  loginForm: FormGroup;
  mensagem: string = '';
  carregando = false;

  constructor(
    private fb: FormBuilder,
    private authService: Auth,
    private router: Router
  ) {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      senha: ['', Validators.required],
    });
  }

  onSubmit() {
    if (this.loginForm.invalid) return;

    this.carregando = true;
    this.mensagem = '';

    const { email, senha } = this.loginForm.value;

    this.authService.login(email, senha).subscribe({
      next: (res) => {
        this.carregando = false;
        if (res.success) {
          this.mensagem = '✅ Login realizado com sucesso!';
          localStorage.setItem('token', res.data.access_token); // salva token se vier
          setTimeout(() => this.router.navigate(['/']), 1000);
        } else {
          this.mensagem = '❌ Email ou senha incorretos.';
        }
      },
      error: () => {
        this.carregando = false;
        this.mensagem = '⚠️ Erro ao conectar com o servidor.';
      },
    });
  }
}
