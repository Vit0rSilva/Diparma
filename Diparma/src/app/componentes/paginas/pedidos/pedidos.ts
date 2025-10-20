import { Component } from '@angular/core';
import { Footer } from '../../layout/footer/footer';
import { Header } from '../../layout/header/header';

@Component({
  selector: 'app-pedidos',
  imports: [Footer, Header],
  templateUrl: './pedidos.html',
  styleUrl: './pedidos.scss'
})
export class Pedidos {

}
