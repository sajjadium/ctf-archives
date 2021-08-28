import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BestAnimesComponent } from './best-animes/best-animes.component';
import { UnderMaintenanceComponent } from './under-maintenance/under-maintenance.component';
import { BestMangasComponent } from './best-mangas/best-mangas.component';

@NgModule({
  declarations: [
    AppComponent,
    BestAnimesComponent,
    UnderMaintenanceComponent,
    BestMangasComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
