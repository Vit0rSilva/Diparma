import { Component } from '@angular/core';
import { Footer } from '../../layout/footer/footer';
import { Header } from '../../layout/header/header';

@Component({
  selector: 'app-principal',
  imports: [Footer, Header],
  templateUrl: './principal.html',
  styleUrl: './principal.scss'
})
export class Principal {

}
