import { HttpClient, HttpParams } from '@angular/common/http';
import { AfterViewInit, Component, OnInit } from '@angular/core';
import { QueryParams } from '@app/models/query';
import { parseQueryParams } from '@app/shared/utils';
import { NzMessageService } from 'ng-zorro-antd/message';
import { Subject, BehaviorSubject, Observable } from 'rxjs';
import { first, takeUntil } from 'rxjs/operators';
import { HomeService } from '../home/home.service';
import { CollectionViewer, DataSource } from '@angular/cdk/collections';
import { environment } from '@environments/environment';

const BASE_URL = environment.authApiURL;

interface ItemData {
  gender: string;
  name: Name;
  email: string;
}

interface Name {
  title: string;
  first: string;
  last: string;
}

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.less']
})
export class DashboardComponent implements OnInit {
  data = [
    'Racing car sprays burning fuel into crowd.',
    'Japanese princess to wed commoner.',
    'Australian walks 100km after outback crash.',
    'Man charged over missing wedding girl.',
    'Los Angeles battles huge wildfires.',
    'Racing car sprays burning fuel into crowd.',
    'Japanese princess to wed commoner.',
    'Australian walks 100km after outback crash.',
    'Man charged over missing wedding girl.',
    'Los Angeles battles huge wildfires.',
    'Racing car sprays burning fuel into crowd.',
    'Japanese princess to wed commoner.',
    'Australian walks 100km after outback crash.',
    'Man charged over missing wedding girl.',
    'Los Angeles battles huge wildfires.',
  ];
  ds = new MyDataSource(this.http);
  // product and product revision
  totalProductPublished: any = 0;
  totalProductDraft: any = 0;
  totalProductPending: any = 0;

  // suppliers
  totalActiveSuppliers: any = 0;
  totalInvitationsSuppliers: any = 0;
  totalInvitationAccepted1days: any = 0;
  totalInvitationAccepted7days: any = 0;
  totalInvitationAccepted30days: any = 0;

  percentInvitationAccepted1days: any = 0;
  percentInvitationAccepted7days: any = 0;
  percentInvitationAccepted30days: any = 0;

  //orders
  totalOrders: any = 0;
  totalOrders1days: any = 0;
  totalOrders7days: any = 0;
  totalOrders30days: any = 0;

  percentOrders1days: any = 0;
  percentOrders7days: any = 0;
  percentOrders30days: any = 0;

  private destroy$ = new Subject();
  constructor(
    private http: HttpClient,
    private nzMessage: NzMessageService,
    private homeService: HomeService
  ) {}
  async ngAfterViewInit() {
    // product
    this.totalProductPublished = await this.homeService.getMentionAdmin().toPromise();
    this.totalProductDraft = await this.homeService.getMentionAdmin().toPromise();

    // product revision
    this.totalProductPending = await this.homeService.getMentionAdmin().toPromise();

    //suppliers


    if (this.totalInvitationsSuppliers > 0) {
      this.percentInvitationAccepted1days =
        (this.totalInvitationAccepted1days * 100) / this.totalInvitationsSuppliers;
      this.percentInvitationAccepted7days =
        (this.totalInvitationAccepted7days * 100) / this.totalInvitationsSuppliers;
      this.percentInvitationAccepted30days =
        (this.totalInvitationAccepted30days * 100) / this.totalInvitationsSuppliers;
    }

    document.getElementById(
      'supplies-1-days'
    )!.style.strokeDasharray = `${this.percentInvitationAccepted1days} , 100`;
    document.getElementById(
      'supplies-7-days'
    )!.style.strokeDasharray = `${this.percentInvitationAccepted7days} , 100`;
    document.getElementById(
      'supplies-30-days'
    )!.style.strokeDasharray = `${this.percentInvitationAccepted30days} , 100`;

    //orders
    let totalOrders: number = 50;
    this.totalOrders = totalOrders;

    let totalOrders1days: number = 10;
    this.totalOrders1days = totalOrders1days;
    let totalOrders7days: number = 15;
    this.totalOrders7days = totalOrders7days;
    let totalOrders30days: number = 25;
    this.totalOrders30days = totalOrders30days;

    if (this.totalOrders > 0) {
      this.percentOrders1days = (this.totalOrders1days * 100) / this.totalOrders;
      this.percentOrders7days = (this.totalOrders7days * 100) / this.totalOrders;
      this.percentOrders30days = (this.totalOrders30days * 100) / this.totalOrders;
      console.log(this.percentOrders1days, this.percentOrders7days, this.percentOrders30days);
    }

    document.getElementById(
      'orders-1-days'
    )!.style.strokeDasharray = `${this.percentOrders1days} , 100`;
    document.getElementById(
      'orders-7-days'
    )!.style.strokeDasharray = `${this.percentOrders7days} , 100`;
    document.getElementById(
      'orders-30-days'
    )!.style.strokeDasharray = `${this.percentOrders30days} , 100`;
  }

  async ngOnInit() {
    this.ds
      .completed()
      .pipe(takeUntil(this.destroy$))
      .subscribe(() => {
        this.nzMessage.warning('Infinite List loaded all');
      });
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  fetchData(params?: QueryParams) {
    console.log('ascasc');
   // return this.homeService.getDataObservable(parseQueryParams(params));
  }
}

class MyDataSource extends DataSource<ItemData> {
  private pageSize = 10;
  private cachedData: ItemData[] = [];
  private fetchedPages = new Set<number>();
  private dataStream = new BehaviorSubject<ItemData[]>(this.cachedData);
  private complete$ = new Subject<void>();
  private disconnect$ = new Subject<void>();
  constructor(private http: HttpClient) {
    super();
  }

  completed(): Observable<void> {
    return this.complete$.asObservable();
  }

  connect(collectionViewer: CollectionViewer): Observable<ItemData[]> {
    this.setup(collectionViewer);
    return this.dataStream;
  }

  disconnect(): void {
    this.disconnect$.next();
    this.disconnect$.complete();
  }

  private setup(collectionViewer: CollectionViewer): void {
    this.fetchPage(0);
    collectionViewer.viewChange
      .pipe(takeUntil(this.complete$), takeUntil(this.disconnect$))
      .subscribe((range) => {
        if (this.cachedData.length >= 100) {
          this.complete$.next();
          this.complete$.complete();
        } else {
          this.fetchPage(range.end + 1);
        }
      });
  }

  private fetchPage(pageIndex: number): void {
    if (this.fetchedPages.has(pageIndex)) {
      return;
    }
    this.fetchedPages.add(pageIndex);

    let _params: QueryParams = {
      pageIndex: pageIndex + 1,
      pageSize: 10,
      sortField: null,
      sortOrder: null,
    };
    console.log(_params);
    this.fetchData(_params)
      ?.pipe(first())
      .subscribe({
        next: (data) => {
          console.log(data);
          this.cachedData.splice(pageIndex * this.pageSize, this.pageSize, ...data.data);
          this.dataStream.next(this.cachedData);
        },
      });
    /*
    this.http
      .get<{ results: ItemData[] }>(
        `https://randomuser.me/api/?results=${this.pageSize}&inc=name,gender,email,nat&noinfo`
      )
      .pipe(catchError(() => of({ results: [] })))
      .subscribe((res) => {
        this.cachedData.splice(page * this.pageSize, this.pageSize, ...res.results);
        this.dataStream.next(this.cachedData);
      });
      */
  }
  fetchData(params?: QueryParams) {
    console.log('ascasc');
    return this.getDataObservable(parseQueryParams(params));
  }
  getDataObservable(params: HttpParams): Observable<any> {
    return this.http.get<any>(`${BASE_URL}/college_year/`,{params: params});
  }
}