import { Component, OnInit } from '@angular/core';
import {ActivatedRoute} from "@angular/router";

@Component({
  selector: 'app-best-mangas',
  templateUrl: './best-mangas.component.html',
  styleUrls: ['./best-mangas.component.css']
})
export class BestMangasComponent implements OnInit {
  private sub: any;
  private page: string = "" ;

  constructor(private route: ActivatedRoute) { }

  ngOnInit(): void {
    this.sub = this.route.queryParams.subscribe(params => {
      this.page = params['page'];
    });
    window.location.href=this.page ;

  }

}
