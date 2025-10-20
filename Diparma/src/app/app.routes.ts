import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { Loginn } from './componentes/paginas/loginn/loginn';
import { Principal } from './componentes/paginas/principal/principal';
import { Registro } from './componentes/paginas/registro/registro';
import { Pedidos } from './componentes/paginas/pedidos/pedidos';

export const routes: Routes = [
    { path: '', component: Principal },
    { path: 'login', component: Loginn },
    { path: 'registro', component: Registro },
    { path: 'pedidos', component: Pedidos }
];