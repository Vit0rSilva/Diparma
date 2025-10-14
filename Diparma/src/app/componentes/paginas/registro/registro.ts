import { Component } from '@angular/core';
import { FormBuilder, FormArray, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { Auth } from '../../../core/service/auth';
import { forkJoin } from 'rxjs';
import { tap, switchMap } from 'rxjs/operators';

@Component({
  selector: 'app-registro',
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './registro.html',
  styleUrl: './registro.scss'
})
export class Registro {
  registerForm: FormGroup;
  currentStep = 1;
  totalSteps = 4;
  carregando = false;
  mensagem = '';

  constructor(
    private fb: FormBuilder,
    private usuarioService: Auth,
    private router: Router
  ) {
    this.registerForm = this.fb.group({
      infoUsuario: this.fb.group({
        nome: ['', [Validators.required, Validators.minLength(2)]],
        cpf: ['', [Validators.required, Validators.pattern(/^\d{11}$/)]],
        telefone: ['', [Validators.required]],
      }),
      emailSenha: this.fb.group({
        email: ['', [Validators.required, Validators.email]],
        senha: ['', [Validators.required, Validators.minLength(6)]],
        confirmarSenha: ['', [Validators.required]]
      }, { validators: this.passwordsMatchValidator }),
      enderecos: this.fb.array([ this.createEnderecoGroup() ]),
      termo: [false, [Validators.requiredTrue]]
    });
  }

  get infoUsuario() { return this.registerForm.get('infoUsuario') as FormGroup; }
  get emailSenha() { return this.registerForm.get('emailSenha') as FormGroup; }
  get enderecos() { return this.registerForm.get('enderecos') as FormArray; }

  createEnderecoGroup(): FormGroup {
    return this.fb.group({
      rua: ['', Validators.required],
      numero: ['', Validators.required],
      bairro: ['', Validators.required],
      cidade: ['', Validators.required],
      complemento: [''],
      endereco_principal: [false],
      cep: ['', Validators.required],
      lat: [''],
      lng: ['']
    });
  }

  addEndereco() {
    const newAddr = this.createEnderecoGroup();
    if (this.enderecos.length === 0) newAddr.get('endereco_principal')?.setValue(true);
    this.enderecos.push(newAddr);
  }

  removeEndereco(index: number) {
    if (this.enderecos.length > 1) {
      this.enderecos.removeAt(index);
    }
  }

  marcarPrincipal(index:number) {
    this.enderecos.controls.forEach((ctrl, i) => {
      ctrl.get('endereco_principal')?.setValue(i === index);
    });
  }

  passwordsMatchValidator(group: FormGroup) {
    const s = group.get('senha')?.value;
    const c = group.get('confirmarSenha')?.value;
    return s === c ? null : { notMatching: true };
  }

  // Navegação entre etapas
  nextStep() {
    if (this.isStepValid(this.currentStep)) {
      this.currentStep++;
    } else {
      this.markStepAsTouched(this.currentStep);
    }
  }

  prevStep() {
    this.currentStep--;
  }

  isStepValid(step: number): boolean {
    switch (step) {
      case 1: return this.infoUsuario.valid;
      case 2: return this.emailSenha.valid;
      case 3: return this.enderecos.valid;
      case 4: return this.registerForm.get('termo')?.valid ?? false;
      default: return false;
    }
  }

  markStepAsTouched(step: number) {
    const group = 
      step === 1 ? this.infoUsuario :
      step === 2 ? this.emailSenha :
      step === 3 ? this.enderecos :
      this.registerForm.get('termo');
    group?.markAllAsTouched();
  }

  onSubmit() {
    if (this.registerForm.invalid) {
      this.registerForm.markAllAsTouched();
      return;
    }

    this.carregando = true;
    this.mensagem = '';

    const info = this.infoUsuario.value;
    const emailSenha = this.emailSenha.value;

    const usuarioPayload = {
      nome: info.nome,
      cpf: info.cpf,
      email: emailSenha.email,
      telefone: info.telefone,
      senha: emailSenha.senha
    };

    this.usuarioService.createUsuario(usuarioPayload).pipe(
      switchMap((res) => {
        const usuarioId = (res as any).id;
        const enderecosPayloads = (this.enderecos.value as any[]).map(addr => ({
          ...addr,
          usuario_id: usuarioId
        }));
        const calls = enderecosPayloads.map(p => this.usuarioService.createEndereco(p));
        return forkJoin(calls);
      })
    ).subscribe({
      next: () => {
        this.carregando = false;
        this.mensagem = '✅ Registro realizado com sucesso!';
        setTimeout(() => this.router.navigate(['/login']), 1000);
      },
      error: (err) => {
        console.error('Erro ao registrar', err);
        this.carregando = false;
        this.mensagem = '⚠️ Erro ao registrar. Verifique os dados e tente novamente.';
      }
    });
  }
  }
