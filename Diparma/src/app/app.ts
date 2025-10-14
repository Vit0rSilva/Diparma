import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Footer } from './componentes/layout/footer/footer';
import { Header } from './componentes/layout/header/header';
import { Principal } from './componentes/paginas/principal/principal';



@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  protected readonly title = signal('Diparma');
}
